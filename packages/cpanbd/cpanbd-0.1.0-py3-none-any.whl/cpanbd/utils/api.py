import importlib.resources as pkg_resources
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

import json5
import requests
from jsonschema import validate
from pydantic import Field, TypeAdapter, dataclasses

from .auth import Auth
from .checkdata import BaseResponse, JsonInput
from .const import BASE_URL, HEADERS


def get_api(filepath: str, *args: Any) -> dict:
    """
    获取 API.

    Args:
        filepath (str): API 所属分类,即 `apijson/***.json`下的文件名(不含后缀名)
        *args (Any): 预留的可选参数(当前未使用).

    Returns:
        dict, 该 API 的内容.
    """
    path = Path(filepath)
    # 如果没有后缀,则添加.json后缀
    if not Path(filepath).suffix:
        path = path.with_suffix(".json")

    # 如果是相对路径,则在当前目录下查找
    # 处理相对路径
    if not path.is_absolute():
        try:
            path = pkg_resources.files("cpanbd.apijson").joinpath(str(path))
            path = Path(str(path))
        except ModuleNotFoundError:
            print("❌ 找不到模块 `cpanbd.apijson`, 请确认路径或依赖包正确")
            sys.exit(1)

    if not path.exists():
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)

    # 读取并校验 JSON 文件
    with open(path, "r", encoding="utf-8") as file:
        try:
            data: dict = json5.load(file)
        except Exception as e:
            print(f"❌ JSON 解析失败: {path}\n错误: {e}")
            sys.exit(1)

    # 校验 JSON 数据
    list_adapter = TypeAdapter(Dict[str, JsonInput])
    list_adapter.validate_python(data)
    # 按参数索引嵌套数据
    for arg in args:
        try:
            data = data[arg]
        except KeyError:
            print(f"❌ 参数 `{arg}` 不存在于 API 数据中")
            sys.exit(1)
    return data


@dataclasses.dataclass
class Api:
    """
    用于请求的 Api 类
    """

    method: str
    url: str
    data: Optional[dict] = Field(default_factory=dict)
    params: Optional[dict] = Field(default_factory=dict)
    schema_: Optional[dict] = Field(default_factory=dict)
    comment: str = ""
    auth: Auth = Field(default_factory=Auth)
    headers: dict = Field(default_factory=dict)
    files: Optional[dict] = Field(default_factory=dict)
    skip: bool = Field(default=False)

    def __post_init__(self) -> None:
        """
        初始化 Api 对象
        """
        # 获取请求方法
        self.method = self.method.upper()
        self.auth = self.auth or Auth()
        self.data = self._replace_values(self.data) or None
        self.params = self._replace_values(self.params) or None
        self.schema_ = self.schema_ or None
        self.headers = self.headers or HEADERS.copy()
        self.files = self.files or None

    def _update_attr(self, attr: str, **kwargs) -> "Api":
        if "skip" in kwargs:
            self.skip = kwargs.pop("skip")
        value = {k: v for k, v in kwargs.items() if v is not None}
        # 如果 v 是 list,则将其转换为 str
        for k, v in value.items():
            if isinstance(v, list):
                value[k] = json5.dumps(v, ensure_ascii=False, separators=(",", ":"))
            elif isinstance(v, dict):
                value[k] = json5.dumps(v, ensure_ascii=False, separators=(",", ":"))
        setattr(self, attr, value)
        return self

    def update_data(self, **kwargs) -> "Api":
        return self._update_attr("data", **kwargs)

    def update_params(self, **kwargs) -> "Api":
        return self._update_attr("params", **kwargs)

    def update_files(self, arg) -> "Api":
        self.files = arg
        return self

    def update_method(self, method: str) -> "Api":
        """
        更新请求方法
        """
        self.method = method.upper()
        return self

    def update_url(self, url: str) -> "Api":
        """
        更新请求 URL
        """
        self.url = url
        return self

    def update_headers(self, **kwargs) -> "Api":
        self.headers = kwargs
        return self

    def _prepare_request(self) -> dict:
        """
        准备请求参数
        """

        headers = self.headers.copy()
        if not self.files:
            headers["Content-Type"] = "application/json"

        full_url = (
            self.url
            if self.url.startswith("http")
            else f"{BASE_URL.rstrip('/')}/{self.url.lstrip('/')}"
        )
        config = {
            "method": self.method,
            "url": full_url,
            "params": self.params,
            "data": self.data,
            "files": self.files,
            "headers": headers,
        }

        config = {k: v for k, v in config.items() if v is not None}
        if config.get("files") is not None:
            config["headers"].pop("Content-Type", None)

        return config

    def request(self, byte: bool = False) -> Union[int, str, dict, bytes, None]:
        """
        发送请求并返回结果

        Args:
            byte (bool): 是否返回字节流,默认为 False
        """
        # 处理请求参数
        config: dict = self._prepare_request()
        for _ in range(5):
            response = requests.request(**config)
            # print("response.url:", response.url)
            response.raise_for_status()
            code = response.json().get("errno", None)
            if code == 31034:
                print("❌ 风控,请稍后再试")
                time.sleep(3)
                continue
            elif code == -1:
                # 权益已过期
                self.auth.refresh_access_token()
            else:
                break

        if byte:
            return response.text

        if self.skip:
            # 如果不需要验证响应数据的 schema_,则直接返回
            return response.json()
        if self.schema_:
            res_json: dict = response.json()
            BaseResponse.model_validate(res_json)
            validate(
                instance=res_json,
                schema=self.schema_,
            )
        return response.json()

    @property
    def result(self) -> Union[int, str, dict, bytes, None]:
        return self.request()

    def _replace_values(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {key: self._replace_values(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_values(item) for item in obj]
        elif isinstance(obj, str):
            return self._process_string(obj)
        else:
            return obj

    def _process_string(self, value: str) -> Any:
        value = value.strip()
        if "None" in value or "null" in value:
            return None

        # 处理可选和必需标记
        if ": optional" in value:
            value = value.replace(": optional", "").strip()
        elif ": required" in value:
            value = value.replace(": required", "").strip()

        # 处理类型转换
        if value.endswith(": int"):
            value = value.replace(": int", "").strip()
            return int(value)
        elif value.endswith(": str"):
            value = value.replace(": str", "").strip()
            return value
        elif value.endswith(": bool"):
            value = value.replace(": bool", "").strip()
            return value.lower() == "true"
        elif value.endswith(": float"):
            value = value.replace(": float", "").strip()
            return float(value)
        elif value.lower() in ("null", "none"):
            return None

        # 处理模板字符串
        if value.startswith("{{") and value.endswith("}}"):
            inner = value[2:-2].strip()
            if inner.lower().startswith("env."):
                env_key = inner[4:]
                env_value = os.getenv(env_key)
                if env_value is None:
                    print(f"❌ 环境变量 `{env_key}` 不存在")
                    sys.exit(1)
                return env_value
            else:
                attr_value = getattr(self.auth, inner, None)
                if attr_value is None:
                    print(f"❌ API `{inner}` 不存在")
                    sys.exit(1)
                return attr_value

        return value


__all__ = [
    "get_api",
    "Api",
    "Auth",
]

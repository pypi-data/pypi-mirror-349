"""获取百度网盘的访问令牌

采用 env 文件来管理授权信息,

- 项目级别的配置文件: `.env`
- 系统级别的配置文件: `~/.env.panbd`

如果两个文件都存在, 则优先使用项目级别的配置文件

需要去[百度开放平台](https://pan.baidu.com/union/console/applist) 申请一个应用, 不提供私人的

配置文件参考如下

```bash
BAIDU_API_APPKEY=xxx   #AppKey
BAIDU_API_SECRETKEY=xxx  #SecretKey
BAIDU_API_APPID=xxx   #AppID
BAIDU_APPNAME=xxx  #应用名称
# 百度规定只能上传到 /apps/{BAIDU_APPNAME} 目录下

```

当有了以上信息以后, 运行下面的代码, 根据提示访问链接, 授权后复制链接中的 code 参数, 粘贴到输入框中即可,后续就不用管了

```python
from cpanbd import Auth
auth = Auth()
```

上面的命令会自动生成下面的环境变量,存储到 `.env` 文件中
```bash
###下面是返回的access_token
BAIDU_ACCESS_TOKEN=
BAIDU_EXPIREDAT=
BAIDU_REFRESH_TOKEN=
```





"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import requests
from dotenv import set_key
from jsonschema import validate
from pydantic import dataclasses
from tenacity import retry, stop_after_attempt, wait_random

from .const import HEADERS, load_env

schema_ = {
    "type": "object",
    "properties": {
        "expires_in": {"type": "number"},
        "refresh_token": {"type": "string"},
        "access_token": {"type": "string"},
        "session_secret": {"type": "string"},
        "session_key": {"type": "string"},
        "scope": {"type": "string"},
    },
    "required": [
        "expires_in",
        "refresh_token",
        "access_token",
        "session_secret",
        "session_key",
        "scope",
    ],
}


@dataclasses.dataclass
class Auth:
    """
    用于获取和设置访问令牌的类.


    """

    access_token: Optional[str] = os.getenv("BAIDU_ACCESS_TOKEN")
    access_expiredAt: Optional[str] = os.getenv("BAIDU_EXPIREDAT")  # ISO8601格式字符串
    access_refresh_token: Optional[str] = os.getenv("BAIDU_REFRESH_TOKEN")

    def __post_init__(self) -> None:
        """
        初始化 Auth 对象
        """
        load_env()

        if not self.access_token:
            # 如果没有 access_token, 需要获取
            self._get_access_token()

    def save_info(self, res: dict) -> None:
        """
        保存 access_token 信息
        """
        # 验证成功,返回 access_token
        self.access_token = res["access_token"]
        timestamp = res["expires_in"] + int(datetime.now().timestamp())
        self.access_expiredAt = datetime.fromtimestamp(timestamp).isoformat()
        self.access_refresh_token = res["refresh_token"]

        # 将 access_token 存入环境文件
        project_env_path = os.path.join(os.getcwd(), ".env")
        system_env_path = os.path.join(os.path.expanduser("~"), ".env.panbd")
        if os.path.exists(project_env_path):
            env_path = project_env_path
        elif os.path.exists(system_env_path):
            env_path = system_env_path
        else:
            # 默认创建项目目录下的 .env
            env_path = project_env_path
            Path(env_path).touch()

        if self.access_token:
            set_key(env_path, "BAIDU_ACCESS_TOKEN", self.access_token)
        if self.access_expiredAt:
            set_key(env_path, "BAIDU_EXPIREDAT", self.access_expiredAt)
        if self.access_refresh_token:
            set_key(env_path, "BAIDU_REFRESH_TOKEN", self.access_refresh_token)

        print(f"✅ access_token 获取成功,并保存: {env_path}")

    def _get_access_token(self) -> "Auth":
        d = {
            "method": "get",
            "url": "https://openapi.baidu.com/oauth/2.0/authorize",
            "params": {
                "response_type": "code",
                "client_id": os.getenv("BAIDU_API_APPKEY"),
                "redirect_uri": "oob",
                "scope": "basic,netdisk",
                "device_id": os.getenv("BAIDU_API_APPID"),
            },
        }
        query_string = urlencode(d["params"])
        url = f"{d['url']}?{query_string}"
        print("请在浏览器中登录您的百度账号并打开下面链接获取 code 参数")
        print(f"\n{url}\n")
        code = input("请输入获得的 code 值:")
        # 访问链接获取 access_token
        d1 = {
            "method": "get",
            "url": "https://openapi.baidu.com/oauth/2.0/token",
            "params": {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": os.getenv("BAIDU_API_APPKEY"),
                "client_secret": os.getenv("BAIDU_API_SECRETKEY"),
                "redirect_uri": "oob",
            },
        }

        # 验证返回值
        try:
            res = requests.request(**d1, headers=HEADERS)
            res.raise_for_status()
            res = res.json()
            validate(instance=res, schema=schema_)
        except Exception as e:
            print(f"❌ access_token 获取失败: {e}")
            sys.exit(1)

        self.save_info(res)
        return self

    def _is_token_expired(self) -> bool:
        """判断 access_token 是否过期"""
        if not self.access_expiredAt:
            return False  # 没有过期时间,认为没过期
        try:
            expire_dt = datetime.fromisoformat(self.access_expiredAt)
            now = datetime.now()
            return now >= expire_dt
        except ValueError:
            print("❌ Invalid access_expiredAt format")
            return True

    @property
    def token(self) -> str | None:
        """
        每次访问时自动检查是否过期并刷新
        """
        if self._is_token_expired():
            print("⚠️ access_token 已过期,正在刷新...")
            self.refresh_access_token()

        return self.access_token

    def set_access_token(self, access_token: str) -> "Auth":
        """
        设置 access_token, 一次性的,不会保存到环境变量中,且不会检查是否过期

        Args:
            access_token (str): 访问令牌
        """
        self.access_token = access_token
        self.access_expiredAt = datetime.fromtimestamp(
            int(datetime.now().timestamp()) + 2592000
        ).isoformat()
        self.access_refresh_token = None

        return self

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=5))
    def refresh_access_token(self) -> "Auth":
        """强制刷新 access_token"""
        d1 = {
            "method": "get",
            "url": "https://openapi.baidu.com/oauth/2.0/token",
            "params": {
                "grant_type": "refresh_token",
                "refresh_token": os.getenv("BAIDU_REFRESH_TOKEN"),
                "client_id": os.getenv("BAIDU_API_APPKEY"),
                "client_secret": os.getenv("BAIDU_API_SECRETKEY"),
            },
        }
        if not d1["params"]["refresh_token"]:
            print("❌ 无法刷新, 请设置环境变量 BAIDU_REFRESH_TOKEN")
            sys.exit(1)
        if not d1["params"]["client_id"]:
            print("❌ 无法刷新, 请设置环境变量 BAIDU_API_APPKEY")
            sys.exit(1)
        if not d1["params"]["client_secret"]:
            print("❌ 无法刷新 , 请设置环境变量 BAIDU_API_SECRETKEY")
            sys.exit(1)

        res = requests.request(**d1, headers=HEADERS)
        try:
            res.raise_for_status()
            res = res.json()
            validate(instance=res, schema=schema_)
        except Exception as e:
            print(f"❌ access_token 刷新失败: {e}")
            sys.exit(1)
        self.save_info(res)
        return self


if __name__ == "__main__":
    auth = Auth()
    print(auth)

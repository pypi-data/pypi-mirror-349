from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator


class BaseResponse(BaseModel):
    """
    基础响应类.
    """

    errno: Literal[0]
    request_id: Optional[Union[str, int]] = None


class JsonInput(BaseModel):
    method: str
    url: str
    data: Optional[Dict] = None
    params: Optional[Dict] = None
    schema_: Optional[Dict] = None
    comment: Optional[str] = None
    response_schema: Optional[Dict] = None
    files: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")  # 禁止额外字段

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        allowed = {"get", "post", "put", "delete"}
        v_lower = v.lower()
        if v_lower not in allowed:
            raise ValueError(f"method 必须是以下之一: {allowed}")
        return v_lower  # 统一返回小写形式

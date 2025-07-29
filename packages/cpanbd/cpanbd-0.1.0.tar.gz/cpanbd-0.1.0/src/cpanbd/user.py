from typing import Any, Literal, Optional

from .utils.api import Auth
from .utils.baseapiclient import BaseApiClient, auto_args_call_api


class User(BaseApiClient):
    def __init__(self, auth: Optional[Auth] = None) -> None:
        super().__init__(filepath="user", auth=auth)

    @auto_args_call_api()
    def uinfo(self, skip: bool = False) -> dict[str, Any] | None:
        """获取用户信息

        本接口用于获取用户的基本信息, 包括账号、头像地址、会员类型等.


        对应百度的API接口: [https://pan.baidu.com/union/doc/pksg0s9ns](https://pan.baidu.com/union/doc/pksg0s9ns)

        Args:
            skip (bool): 是否跳过检查

        """

    @auto_args_call_api()
    def quota(
        self,
        checkfree: Literal[0, 1] = 0,
        checkexpire: Literal[0, 1] = 0,
        skip: bool = False,
    ) -> dict[str, Any] | None:
        """获取网盘容量信息

        本接口用于获取用户的网盘空间的使用情况, 包括总空间大小, 已用空间和剩余可用空间情况.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Cksg0s9ic](https://pan.baidu.com/union/doc/Cksg0s9ic)

        Args:
            checkfree (Literal[0, 1]): 是否检查免费信息, 0为不查, 1为查, 默认为0
            checkexpire (Literal[0, 1]): 是否检查过期信息, 0为不查, 1为查, 默认为0
            skip (bool): 是否跳过检查
        """


if __name__ == "__main__":
    user = User()
    print(user.uinfo())

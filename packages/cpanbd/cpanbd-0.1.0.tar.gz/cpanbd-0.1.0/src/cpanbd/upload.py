from typing import Any, Literal, Optional

from .utils.api import Auth
from .utils.baseapiclient import BaseApiClient, auto_args_call_api


class Upload(BaseApiClient):
    def __init__(self, auth: Optional[Auth] = None) -> None:
        super().__init__(filepath="upload", auth=auth)

    @auto_args_call_api()
    def precreate(
        self,
        path: str,
        size: int,
        isdir: Literal[0, 1],
        block_list: list[str] | str,
        rtype: Literal[1, 2, 3] = 1,
        uploadid: Optional[str] = None,
        content_md5: Optional[str] = None,
        slice_md5: Optional[str] = None,
        local_ctime: Optional[int] = None,
        local_mtime: Optional[int] = None,
        skip: bool = False,
    ) -> dict[str, Any] | None:
        """预上传

        预上传是通知网盘云端新建一个上传任务, 网盘云端返回唯一ID uploadid 来标识此上传任务.

        对应百度的API接口: [https://pan.baidu.com/union/doc/3ksg0s9r7](https://pan.baidu.com/union/doc/3ksg0s9r7)

        Args:
            path (str): 上传的文件或目录的路径
            size (int): 文件和目录两种情况:上传文件时, 表示文件的大小, 单位B；上传目录时, 表示目录的大小, 目录的话大小默认为0
            isdir (Literal[0, 1]): 是否为目录, 0 文件, 1 目录
            block_list (list): 分片上传时, 分片列表, 分片大小为4MB, 最大支持10000个分片
            rtype (Optional[Literal[1, 2]]): 文件命名策略. 1 表示当path冲突时, 进行重命名 //2 表示当path冲突且block_list不同时, 进行重命名
            uploadid (Optional[str]): 上传ID
            content_md5 (Optional[str]): 文件MD5, 32位小写
            slice_md5 (Optional[str]): 文件校验段的MD5, 32位小写, 校验段对应文件前256KB
            local_ctime (Optional[int]): 客户端创建时间,  默认为当前时间戳
            local_mtime (Optional[int]): 客户端修改时间,  默认为当前时间戳
            skip (bool): 是否跳过上传
        """

    @auto_args_call_api()
    def upload(
        self,
        url: str,
        path: str,
        uploadid: str,
        partseq: int,
        files: Any,
        skip: bool = True,  # 因为只返回两个值
        type: str = "tmpfile",  # 固定值
    ) -> dict[str, Any] | None:
        """分片上传
        本接口用于将本地文件上传到网盘云端服务器.


        文件分两种类型:小文件, 是指文件大小小于等于4MB的文件, 成功调用一次本接口后, 表示分片上传阶段完成；大文件, 是指文件大小大于4MB的文件, 需要先将文件按照4MB大小进行切分, 然后针对切分后的分片列表, 逐个分片进行上传, 分片列表的分片全部成功上传后, 表示分片上传阶段完成.

        根据不同的用户等级有不同的限制

        对应百度的API接口: [https://pan.baidu.com/union/doc/nksg0s9vi](https://pan.baidu.com/union/doc/nksg0s9vi)

        Args:
            path (str): 上传的文件的路径
            uploadid (str): 上传ID
            partseq (int): 分片序号, 从0开始
            files (Any): 上传的文件对象
            skip (bool): 是否跳过上传

        """

    @auto_args_call_api()
    def create(
        self,
        path: str,
        size: str,
        isdir: Literal["0", "1"],
        block_list: list[str] | str,
        uploadid: str,
        rtype: Literal[1, 2, 3] = 1,
        local_ctime: Optional[int] = None,
        local_mtime: Optional[int] = None,
        zip_quality: Optional[Literal[50, 70, 100]] = None,
        zip_sign: Optional[int] = None,
        is_revision: Optional[int] = 0,
        mode: Optional[Literal[0, 1, 2, 3, 4, 5]] = None,
        exif_info: Optional[str] = None,
        skip: bool = False,
    ) -> dict[str, Any] | None:
        """创建文件

        本接口用于将多个文件分片合并成一个文件, 生成文件基本信息, 完成文件的上传最后一步.


        对应百度的API接口: [https://pan.baidu.com/union/doc/rksg0sa17](https://pan.baidu.com/union/doc/rksg0sa17)

        Args:
            path (str): 上传的文件或目录的路径
            size (str): 文件和目录两种情况:上传文件时, 表示文件的大小, 单位B；上传目录时, 表示目录的大小, 目录的话大小默认为0
            isdir (Literal[0, 1]): 是否为目录, 0 文件, 1 目录
            block_list (list[str] | str):  文件各分片md5数组的json串
            uploadid (str): 预上传precreate接口下发的uploadid
            rtype (Literal[1, 2, 3]): 文件命名策略.

                - 1 表示当path冲突时, 进行重命名
                - 2 表示当path冲突且block_list不同时, 进行重命名
                - 3 为覆盖, 需要与预上传precreate接口中的rtype保持一致
            local_ctime (Optional[int]): 客户端创建时间,  默认为当前时间戳
            local_mtime (Optional[int]): 客户端修改时间,  默认为当前时间戳
            zip_quality (Optional[Literal[50, 70, 100]]): 图片压缩程度, 有效值50、70、100, (与zip_sign一起使用)
            zip_sign (Optional[int]): 未压缩原始图片文件真实md5(与zip_quality一起使用)
            is_revision (Optional[int]): 是否需要多版本支持, 1为支持, 0为不支持,  默认为0 (带此参数会忽略重命名策略)
            mode (Optional[Literal[0, 1, 2, 3, 4, 5]]): 上传方式

                - 1 手动、
                - 2 批量上传
                - 3 文件自动备份
                - 4 相册自动备份
                - 5 视频自动备份
            exif_info (Optional[str]): json字符串, orientation、width、height、recovery为必传字段, 其他字段如果没有可以不传
            skip (bool): 是否跳过上传
        """

    @auto_args_call_api()
    def locateupload(
        self,
        path: str,
        uploadid: str,
        skip: bool = False,
    ) -> dict[str, Any] | None:
        """获取上传域名

        本接口用于获取上传域名.

        上传文件数据时, 需要先通过此接口获取上传域名. 可使用返回结果servers字段中的 https 协议的任意一个域名.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Mlvw5hfnr](https://pan.baidu.com/union/doc/Mlvw5hfnr)

        Args:
            path (str): 上传后使用的文件绝对路径
            uploadid (str): 上传ID
            skip (bool): 是否跳过上传
        """
        pass

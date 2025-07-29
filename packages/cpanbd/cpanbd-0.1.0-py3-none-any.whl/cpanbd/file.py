from typing import Any, Literal, Optional

from .utils.api import Auth
from .utils.baseapiclient import BaseApiClient, auto_args_call_api


class File(BaseApiClient):
    def __init__(self, auth: Optional[Auth] = None) -> None:
        super().__init__(filepath="file", auth=auth)

    @auto_args_call_api()
    def list_files(
        self,
        dir: str = "/",
        order: Literal["name", "size", "time"] = "name",
        desc: int = 1,
        start: int = 0,
        limit: int = 100,
        web: int = 1,
        folder: int = 0,
        showempty: int = 0,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取文件列表


        本接口用于获取用户网盘中指定目录下的文件列表. 返回的文件列表支持排序、分页等操作. (不递归,只能是当前目录下的文件列表)

        对应百度的API接口: [https://pan.baidu.com/union/doc/nksg0sat9](https://pan.baidu.com/union/doc/nksg0sat9)


        Args:
            dir (str): 目录名称绝对路径, 必须/开头；
            order (str): 排序方式, 默认为name, 可选值为name, size, time
            desc (int): 是否降序, 0为升序, 1为降序, 默认为1
            start (int): 起始位置, 默认为0
            limit (int): 返回数量, 查询数目, 默认为1000
            web (int): 是否web模式, 默认为1,  为1时返回缩略图地址
            folder (int): 是否只显示文件夹, 默认为0,  为1时只显示文件夹
            showempty (int): 是否显示空文件夹, 默认为0,  为1时显示空文件夹
            skip (bool): 是否跳过检查, 默认为False

        Returns:
            dict: 返回的文件列表, 包含文件名、文件大小、文件类型等信息
        """

    @auto_args_call_api()
    def listall(
        self,
        path: str = "/",
        recursion: int = 0,
        order: Literal["name", "size", "time"] = "name",
        desc: int = 0,
        start: int = 0,
        limit: int = 100,
        ctime: Optional[int] = None,
        mtime: Optional[int] = None,
        web: int = 0,
        device_id: Optional[str] = None,
        skip=False,
    ) -> dict[str, Any] | None:
        """递归获取文件列表

        本接口可以递归获取指定目录下的文件列表. 当目录下存在文件夹, 并想获取到文件夹下的子文件时, 可以设置 recursion 参数为1, 即可获取到更深目录层级的文件.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Zksg0sb73](https://pan.baidu.com/union/doc/Zksg0sb73)

        Args:
            path (str): 目录名称绝对路径, 必须/开头；
            recursion (int): 是否递归,0为否, 1为是, 默认为0
            order (str): 排序方式, 默认为name, 可选值为name, size, time
            desc (int): 是否降序, 0为升序, 1为降序, 默认为0
            start (int): 起始位置, 默认为0
            limit (int): 返回数量, 查询数目, 默认为1000
            ctime (int): 创建时间, 文件上传时间, 设置此参数, 表示只返回上传时间大于ctime的文件
            mtime (int): 修改时间, 文件修改时间, 设置此参数, 表示只返回修改时间大于mtime的文件
            web (int): 是否web模式, 默认为0,  为1时返回缩略图地址
            device_id (str): 设备ID, 硬件设备必传
            skip (bool): 是否跳过检查, 默认为False

        其他参数请参考API文档
        """

    @auto_args_call_api()
    def doclist(
        self,
        parent_path: str = "/",
        page: int = 1,
        num: int = 100,
        order: Literal["name", "size", "time"] = "name",
        desc: int = 1,
        recursion: int = 0,
        web: int = 0,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取文档列表

        本接口用于获取用户指定目录下的文档列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Eksg0saqp](https://pan.baidu.com/union/doc/Eksg0saqp)


        Args:
            parent_path (str): 目录名称绝对路径, 必须/开头；
            page (int): 页码, 从1开始,  如果不指定页码, 则为不分页模式, 返回所有的结果. 如果指定page参数, 则按修改时间倒序排列
            num (int): 一页返回的文档数,  默认值为1000, 建议最大值不超过1000
            order (str): 排序字段: time(修改时间), name(文件名), size(文件大小)
            desc (int): 0为升序, 1为降序, 默认为1
            recursion (int): 是否需要递归, 0为不需要, 1为需要, 默认为0, 递归是指:当目录下有文件夹, 使用此参数, 可以获取到文件夹下面的文档
            web (int): 是否web模式, 默认为0,  为1时返回缩略图地址

        """

    @auto_args_call_api()
    def imagelist(
        self,
        parent_path: str = "/",
        page: int = 1,
        num: int = 100,
        order: Literal["name", "size", "time"] = "name",
        desc: int = 1,
        recursion: int = 0,
        web: int = 0,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取图片列表

        本接口用于获取用户指定目录下的图片列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/bksg0sayv](https://pan.baidu.com/union/doc/bksg0sayv)

        Args:
            parent_path (str): 目录名称绝对路径, 必须/开头；
            page (int): 页码, 从1开始,  如果不指定页码, 则为不分页模式, 返回所有的结果. 如果指定page参数, 则按修改时间倒序排列
            num (int): 一页返回的文档数,  默认值为1000, 建议最大值不超过1000
            order (str): 排序字段: time(修改时间), name(文件名), size(文件大小)
            desc (int): 0为升序, 1为降序, 默认为1
            recursion (int): 是否需要递归, 0为不需要, 1为需要, 默认为0, 递归是指:当目录下有文件夹, 使用此参数, 可以获取到文件夹下面的文档
            web (int): 是否web模式, 默认为0,  为1时返回缩略图地址

        其他参数请参考API文档

        """

    @auto_args_call_api()
    def videolist(
        self,
        parent_path: str = "/",
        page: int = 1,
        num: int = 100,
        order: Literal["name", "size", "time"] = "name",
        desc: int = 1,
        recursion: int = 0,
        skip=False,
        web: int = 1,
    ) -> dict[str, Any] | None:
        """获取视频列表

        本接口用于获取用户指定目录下的视频列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Sksg0saw0](https://pan.baidu.com/union/doc/Sksg0saw0)

        Args:
            parent_path (str): 目录名称绝对路径, 必须/开头；
            page (int): 页码, 从1开始,  如果不指定页码, 则为不分页模式, 返回所有的结果. 如果指定page参数, 则按修改时间倒序排列
            num (int): 一页返回的文档数,  默认值为1000, 建议最大值不超过1000
            order (str): 排序字段: time(修改时间), name(文件名), size(文件大小)
            desc (int): 0为升序, 1为降序, 默认为1
            recursion (int): 是否需要递归, 0为不需要, 1为需要, 默认为0, 递归是指:当目录下有文件夹, 使用此参数, 可以获取到文件夹下面的文档
            web (int): 是否web模式, 默认为1,  为1时返回缩略图地址

        其他参数请参考API文档

        """

    @auto_args_call_api()
    def btlist(
        self,
        parent_path: str = "/",
        page: int = 1,
        num: int = 100,
        order: Literal["name", "size", "time"] = "name",
        desc: int = 1,
        recursion: int = 0,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取bt列表

        本接口用于获取用户指定目录下的bt列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/xksg0sb1d](https://pan.baidu.com/union/doc/xksg0sb1d)

        Args:
            parent_path (str): 目录名称绝对路径, 必须/开头；
            page (int): 页码, 从1开始,  如果不指定页码, 则为不分页模式, 返回所有的结果. 如果指定page参数, 则按修改时间倒序排列
            num (int): 一页返回的文档数,  默认值为1000, 建议最大值不超过1000
            order (str): 排序字段: time(修改时间), name(文件名), size(文件大小)
            desc (int): 0为升序, 1为降序, 默认为1
            recursion (int): 是否需要递归, 0为不需要, 1为需要, 默认为0, 递归是指:当目录下有文件夹, 使用此参数, 可以获取到文件夹下面的文档

        其他参数请参考API文档
        """

    @auto_args_call_api()
    def categoryinfo(
        self,
        category: int = 4,
        parent_path: str = "/",
        recursion: int = 0,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取分类文件总个数

        本接口用于获取用户指定目录下指定类型的文件数量.

        对应百度的API接口: [https://pan.baidu.com/union/doc/dksg0sanx](https://pan.baidu.com/union/doc/dksg0sanx)

        Args:
            category (int): 文件类型, 1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子
            parent_path (str): 目录名称绝对路径, 必须/开头；
            recursion (int): 是否递归, 0 不递归、1 递归, 默认0

        """

    @auto_args_call_api()
    def categorylist(
        self,
        category: str = "1",
        parent_path: str = "/",
        recursion: int = 0,
        ext: Optional[str] = None,
        start: int = 0,
        limit: int = 100,
        order: Literal["name", "size", "time"] = "name",
        desc: str = "0",
        device_id: Optional[str] = None,
        skip=False,
    ) -> dict[str, Any] | None:
        """获取分类文件列表

        本接口用于获取用户目录下指定类型的文件列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Sksg0sb40](https://pan.baidu.com/union/doc/Sksg0sb40)


        Args:
            category (str): 文件类型, 1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子, 多个category使用英文逗号分隔, 示例:3,4
            parent_path (str): 目录名称绝对路径, 必须/开头；
            recursion (int): 是否递归, 0 不递归、1 递归, 默认0
            ext (str): 需要的文件格式, 多个格式以英文逗号分隔, 示例: txt,epub, 默认为category下所有格式
            start (int): 查询起点, 默认为0, 当返回has_more=1时, 应使用返回的cursor作为下一次查询的起点
            limit (int): 查询条数, 默认为1000, 最大值为1000
            order (str): 排序字段: time(修改时间), name(文件名), size(文件大小)
            desc (str): 0为升序, 1为降序, 默认为0
            device_id (str): 设备ID, 硬件设备必传
        其他参数请参考API文档

        """

    @auto_args_call_api()
    def search(
        self,
        key: str = "",
        dir: str = "/",
        category: int = 4,
        num: int = 500,  # 不能修改
        recursion: int = 0,
        web: int = 0,
        device_id: Optional[str] = None,
        skip=False,
    ) -> dict[str, Any] | None:
        """搜索文件

        本接口用于获取用户指定目录下, 包含指定关键字的文件列表.

        对应百度的API接口: [https://pan.baidu.com/union/doc/zksg0sb9z](https://pan.baidu.com/union/doc/zksg0sb9z)

        Args:
            key (str): 搜索关键字, 支持模糊搜索
            dir (str): 目录名称绝对路径, 必须/开头；
            category (int): 文件类型, 1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子
            num (int): 一页返回的文档数,  不能修改
            recursion (int): 是否需要递归, 0为不需要, 1为需要, 默认为0, 递归是指:当目录下有文件夹, 使用此参数, 可以获取到文件夹下面的文档
            web (int): 是否web模式, 默认为0,  为1时返回缩略图地址
            device_id (str): 设备ID, 硬件设备必传
            skip (bool): 是否跳过检查, 默认为False

        其他参数请参考API文档

        """

    @auto_args_call_api()
    def filemetas(
        self,
        fsids: str | list[int],
        dlink: int = 1,
        path: Optional[str] = None,
        thumb: int = 0,
        extra: int = 0,
        needmedia: int = 0,
        detail: int = 0,
        device_id: Optional[str] = None,
        from_apaas: int = 1,
        skip=False,
    ) -> dict[str, Any] | None:
        """查询文件信息

        本接口可用于获取用户指定文件的meta信息. 支持查询多个或一个文件的meta信息, meta信息包括文件名字、文件创建时间、文件的下载地址等.

        对应百度的API接口: [https://pan.baidu.com/union/doc/Fksg0sbcm](https://pan.baidu.com/union/doc/Fksg0sbcm)

        Args:
            fsids (list[int]): 文件id数组, 数组中元素是uint64类型, 数组大小上限是:100, 需要用 json.dumps() 转换为字符串
            dlink (int): 是否需要下载地址, 0为否, 1为是, 默认为0. 获取到dlink后
            path (str): 目录名称绝对路径, 必须/开头；
            thumb (int): 是否需要缩略图, 0为否, 1为是, 默认为0
            extra (int): 是否需要额外信息, 0为否, 1为是, 默认为0
            needmedia (int): 视频是否需要展示时长信息, needmedia=1时, 返回 duration 信息时间单位为秒 （s）, 转换为向上取整.
            detail (int): 视频是否需要展示长, 宽等信息. 0 否、1 是, 默认0
            device_id (str): 设备ID, 硬件设备必传
            from_apaas (int): 1
            skip (bool): 是否跳过检查, 默认为False

        其他参数请参考API文档
        """

    @auto_args_call_api()
    def filemanager(
        self,
        opera: Literal["copy", "move", "rename", "delete"],
        filelist: list[dict[str, Any]],
        aasync: Literal[0, 1, 2] = 1,
        ondup: Literal["fail", "newcopy", "overwrite", "skip"] = "fail",
        device_id: Optional[str] = None,
        skip=False,
    ) -> dict[str, Any] | None:
        """管理文件

        本接口用于对文件进行操作, 包括复制、移动、重命名、删除等操作.

        对应百度的API接口: [https://pan.baidu.com/union/doc/mksg0s9l4](https://pan.baidu.com/union/doc/mksg0s9l4)

        Args:
            opera (str): 文件操作参数, 可实现文件复制、移动、重命名、删除, 依次对应的参数值为: copy, move, rename, delete
            aasync (int): 0 同步, 1 自适应, 2 异步
            filelist (list[dict]): 文件操作列表, 数组中元素是object类型, 数组大小上限是:100
            ondup (str): 全局ondup,遇到重复文件的处理策略, fail(默认, 直接返回失败)、newcopy(重命名文件)、overwrite、skip
            device_id (str): 设备ID, 硬件设备必传
            skip (bool): 是否跳过检查, 默认为False
        其他参数请参考API文档

        filelist 参数示例:

            ```
            [{"path":"/test/123456.docx","dest":"/test/abc","newname":"11223.docx"}]【copy/move示例】

            [{"path":"/test/123456.docx","newname":"123.docx"}]【rename示例】

            ["/test/123456.docx"]【delete示例】
            ```

        """

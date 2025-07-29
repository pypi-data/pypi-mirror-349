import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Literal, Optional

from pydantic import validate_call

from .upload import Upload
from .utils.md5 import (
    calculate_md5,
    calculate_slice_md5,
    encrypt_md5,
    get_file_md5_blocks,
)


class UploadFile:
    """上传文件类, 负责将本地文件分片上传到百度网盘.  (使用多线程上传)

    Attributes:
        up (Upload): 上传对象的实例.

    Example:
    ```python
    from cpanbd import UploadFile, APPNAME

    pan = UploadFile()
    local_filename = "tdata/xxx/Robot0309.zip"
    upload_path = f"/apps/{APPNAME}/tdata/xxx/Robot0309.zip"
    # 上传文件到网盘
    pan.upload_file(
        local_filename=local_filename,
        upload_path=upload_path,
        isdir=0,
        rtype=1,
        bs=32,
        show_progress=True,
    )
    # 如果要批量,只需要循环即可
    ```
    """

    def __init__(self):
        self.up = Upload()

    def upload_part(
        self,
        server_url: str,
        upload_path: str,
        uploadid: str,
        idx: int,
        chunk: bytes,
        expected_md5: str,
        progress: dict,
        show_progress: bool = True,
    ) -> int:
        """
        上传单个文件分片并更新上传进度.

        Args:
            server_url (str): 上传服务器的 URL.
            upload_path (str): 文件在网盘中的目标路径.
            uploadid (str): 上传会话的 ID.
            idx (int): 当前分片的索引.
            chunk (bytes): 当前分片的二进制数据.
            expected_md5 (str): 当前分片的预期 MD5 值.
            progress (Dict[str, object]): 包含上传进度信息的字典.

        Returns:
            int: 成功上传的分片索引.

        Raises:
            Exception: 如果上传失败或 MD5 校验不一致.
        """
        files = [("file", ("part", chunk))]
        res = self.up.upload(
            url=server_url + "/rest/2.0/pcs/superfile2",
            path=upload_path,
            uploadid=uploadid,
            partseq=idx,
            files=files,
        )
        if not res or not res.get("md5"):
            raise Exception(f"上传分片失败: {res}")
        if res["md5"] != expected_md5:
            raise Exception(
                f"分片 {idx} 的 MD5 不一致: 预期 {expected_md5}, 实际 {res['md5']}"
            )

        if progress["lock"]:
            progress["uploaded"] += 1
            if show_progress:
                percent = (progress["uploaded"] / progress["total"]) * 100
                print(f"\r上传进度: {percent:.2f}%", end="", flush=True)
        return idx

    @validate_call
    def upload_file(
        self,
        local_filename: str,
        upload_path: str,
        isdir: Literal[0, 1] = 0,
        rtype: Literal[1, 2, 3] = 1,
        max_workers: Optional[int] = None,
        bs: Literal[4, 16, 32] = 4,
        show_progress: bool = True,
    ) -> None | dict:
        """
        使用多线程方式将本地文件上传到百度网盘.

        Args:
            local_filename (str): 本地文件的路径.
            upload_path (str): 文件在网盘中的目标路径.
            isdir (Literal[0, 1]): 是否为目录, 0 表示文件, 1 表示目录.
            rtype (Literal[1, 2, 3]): 文件命名策略, 默认为 1.
                1: 当path冲突时, 进行重命名
                2: 当path冲突且block_list不同时, 进行重命名
                3: 当云端存在同名文件时, 对该文件进行覆盖
            bs (Literal[4, 16, 32]): 分片大小, 单位为 MB, 默认为 4MB.
            max_workers (int): 最大并发线程数, 默认为 4.
            show_progress (bool): 是否显示上传进度, 默认为 True.

        Returns:
            None
        """
        block_size = 4 * 1024 * 1024  # 4MB

        file_path = Path(local_filename)
        file_size = file_path.stat().st_size

        content_md5 = encrypt_md5(calculate_md5(file_path))
        slice_md5 = calculate_slice_md5(file_path)
        block_list = get_file_md5_blocks(file_path, block_size=block_size)

        # 预创建文件
        res1 = self.up.precreate(
            path=upload_path,
            size=file_size,
            isdir=isdir,
            block_list=block_list,
            rtype=rtype,
            content_md5=content_md5,
            slice_md5=slice_md5,
        )
        if not res1 or res1.get("errno") != 0:
            print(f"预创建失败: {res1}")
            return
        uploadid = res1["uploadid"]
        # 获取上传地址
        res2 = self.up.locateupload(
            path=upload_path,
            uploadid=uploadid,
        )

        if not res2 or not res2.get("servers"):
            print(f"获取上传地址失败: {res2}")
            return
        server_url = res2["servers"][0]["server"]

        # 多线程上传分片
        # 计算可用的线程数
        m = os.cpu_count() or 1
        max_workers = m - 1 if max_workers is None else max_workers
        max_workers = min(max_workers, len(block_list))
        # print(f"开始多线程上传分片, 线程数: {max_workers}")
        progress: dict = {"uploaded": 0, "total": len(block_list), "lock": Lock()}
        with file_path.open("rb") as f:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for idx, expected_md5 in enumerate(block_list):
                    f.seek(idx * block_size)
                    chunk = f.read(block_size)
                    if not chunk:
                        break  # 文件读取完毕
                    future = executor.submit(
                        self.upload_part,
                        server_url,
                        upload_path,
                        uploadid,
                        idx,
                        chunk,
                        expected_md5,
                        progress,
                        show_progress,
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        idx = future.result()
                    except Exception as e:
                        print(f"\n分片上传失败: {e}")
                        return

        # 创建文件
        res3 = self.up.create(
            path=str(upload_path),
            size=str(file_size),
            isdir="0" if isdir == 0 else "1",
            block_list=json.dumps(block_list, separators=(",", ":")),
            uploadid=str(uploadid),
            rtype=rtype,
        )
        print("\n✅ 所有分片上传完成")
        return res3

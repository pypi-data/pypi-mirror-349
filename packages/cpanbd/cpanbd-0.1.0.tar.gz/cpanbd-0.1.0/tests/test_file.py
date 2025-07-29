from cpanbd.file import File

file = File()


def test_file():
    """
    测试用户信息
    """
    res = file.list_files()
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["list"]))


def test_listall():
    """
    测试用户信息
    """
    res = file.listall(path="/", recursion=1, order="name", desc=0, start=0, limit=100)
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["list"]))


def test_doclist():
    """
    测试文档文件列表.
    """
    res = file.doclist(
        parent_path="/", page=1, num=10, order="name", desc=1, recursion=1, web=0
    )
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["info"]))


def test_imagelist():
    """
    测试图片文件列表.
    """
    res = file.imagelist(
        parent_path="/", page=1, num=10, order="name", desc=1, recursion=1, web=0
    )
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["info"]))


def test_videolist():
    """
    测试视频列表.
    """
    res = file.videolist(
        parent_path="/", page=1, num=10, order="name", desc=1, recursion=1
    )
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["info"]))


def test_btlist():
    """
    测试bt文件列表.
    """
    res = file.btlist(
        parent_path="/", page=1, num=10, order="name", desc=1, recursion=1
    )
    print(res)
    assert res is not None, "返回结果为空"
    print(len(res["info"]))


def test_categoryinfo():
    """
    测试获取分类信息
    """
    res = file.categoryinfo(category=4, parent_path="/", recursion=1)
    print(res)
    assert res is not None, "返回结果为空"
    # print(len(res["info"]))


def test_categorylist():
    """
    测试获取分类列表
    """
    res = file.categorylist(category="4", parent_path="/", recursion=1)
    print(res)
    assert res is not None, "返回结果为空"
    # print(len(res["info"]))


def test_search():
    """
    测试获取分类列表
    """
    res = file.search(key="python", category=4, dir="/", recursion=1)
    print(res)
    assert res is not None, "返回结果为空"


def test_filemetas():
    """
    测试获取分类列表
    """

    fsids = [1028540724123072, 426026092779461]
    # fsids = json.dumps(fsids)
    # print(fsids)
    res = file.filemetas(fsids=fsids, dlink=1)
    print(res)
    assert res is not None, "返回结果为空"


##### 暂不测试
# def test_filemanager():
#     """
#     测试获取分类列表
#     """

#     fsids = [1028540724123072, 426026092779461]
#     # fsids = json.dumps(fsids)
#     # print(fsids)
#     res = file.filemanager(fsids=fsids, dlink=1)
#     print(res)
#     assert res is not None, "返回结果为空"


# if __name__ == "__main__":
#     test_file()
#     test_listall()
#     test_doclist()
#     test_imagelist()
#     test_videolist()
#     test_btlist()
#     test_categoryinfo()
#     test_categorylist()
#     test_search()
#     test_filemetas()

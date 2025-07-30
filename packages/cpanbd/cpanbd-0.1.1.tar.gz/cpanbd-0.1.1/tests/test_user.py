from cpanbd.user import User

user = User()


def test_user():
    """
    测试用户信息
    """
    res = user.uinfo()
    assert res is not None, "返回结果为空"
    assert res["errno"] == 0, "返回结果错误"


def test_quota():
    """
    测试用户配额
    """
    res = user.quota()
    assert res is not None, "返回结果为空"
    assert res["errno"] == 0, "返回结果错误"


if __name__ == "__main__":
    # test_user()
    test_quota()

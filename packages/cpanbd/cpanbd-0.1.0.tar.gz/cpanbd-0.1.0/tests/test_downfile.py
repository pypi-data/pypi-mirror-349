from cpanbd.downfile import DownFile

pan = DownFile()


def test_downfile1():
    m = "/我的资源/Y1401-书柜图纸"
    pan.downdir(m, "tmp", overwrite=False, verbose=True)


# def test_downfile2():
#     # md5 验证不通过,但是奇怪的是下载下来的文件可以正确打开
#     # 里面的文件也可以正常使用
#     # 难道文件太大? 解密函数有问题?
#     pan.downfile("/yidun.tar.gz", "yidun.tar.gz")

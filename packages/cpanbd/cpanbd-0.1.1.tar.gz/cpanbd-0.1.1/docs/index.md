# Welcome to cpanbd


百度云盘的python接口文档(非官方), 只实现了部分接口, 仅供学习使用


百度云盘的官方接口文档: [https://pan.baidu.com/union/doc/pksg0s9ns](https://pan.baidu.com/union/doc/pksg0s9ns)

关于授权参考: [Auth](./auth.md)

## 安装

```python
pip install cpanbd
```

## 接口

- 参考接口类



## 常用功能
```python
from cpanbd import DownFile

pan = DownFile()
# 下载文件和目录
pan.downfile("/xxx.txt", "xx.txt")
pan.downdir("/xxx", "xx")

# 把百度的文件秒传到 123(不会下载,不成功则返回False)
## 依赖 pip install  cpan123
from cpanbd import baiduTo123
# 百度网盘文件路径
filebd = "/BaiduNetdiskDownload/book/pdf/xxx.pdf"
# 123网盘文件路径
file123 = "/book/pdf/xxxx.pdf"
baiduTo123(filebd, file123)
``` 


### 封装的接口

- [x] 上传文件
- [x] 下载文件(夹)
- [x] 百度文件秒传到123


### 已实现的接口

1. 网盘基础服务
    - [x] 获取用户信息
    - [x] 获取网盘容量信息
    - [x] 获取文件信息
    - [x] 上传
    - [x] 下载
    - [x] 创建文件夹
    - [ ] 播单能力
    - [ ] 文件分享服务(新)
    - [ ] 最近服务
    
2. ......


## Bug 反馈

- 本人编程能力有限,程序可能会有bug,如果有问题请反馈

- 如果有好的建议,也欢迎反馈 [Issues](https://github.com/zoushucai/cpanbd/issues)



## 为女朋友做的那点事儿（python篇）
Do something for my girly.

[![python version](https://img.shields.io/badge/python-v3.7-blue.svg)](http://python.org/)
![](https://img.shields.io/badge/Window-green.svg)

pythonbar 是基于 python 的常用功能示例合集。

## 环境

- Python 3.7
- Mac/Linux/Windows

### 主要目录

Type 1

- [A-1. 抓取腾讯应用宝App信息并生成excel表记录导出](./A-1.appstore/)

Type 2

- [D-1. 多方式抓取美女福利图片到本地](./D-1.nvshens/)

Type 3

- [G-1. 正经事](./G-1.analysis/)


##常见问题
- ```UnicodeEncodeError: 'gbk' codec can't encode character '\u2022' in position 149: illegal multibyte sequence```

    其实print()函数的局限就是Python默认编码的局限，因为系统是win的，python的默认编码不是'utf-8',改一下python的默认编码成'utf-8'就行了,即修改```sys.stdout```，参考[A-1](./A-1.appstore/)

- 缺少包，请执行```pip install xxx```, xxx代表所需的包名

## 注意

本项目属于个人兴趣开发，开源出来是为了技术交流，请勿使用此项目用于其他违法用途。

如有疑问或见解，欢迎 [Issues](https://github.com/sanplit/pythonbar/issues) .

## 鸣谢

感谢[天行数据](https://www.tianapi.com/)提供，天气，土味情话，智能机器人 api 等接口

## 捐助

如果您认为这个项目对你有所帮助，请我喝杯阿萨姆吧~  🎉

感谢您的支持！

捐助方法如下：
<div style="display: flex;justify-content: flex-start">
<img width="300" height="300" src="./static/imgs/wxpay2.png" />
<img width="300" height="300" src="./static/imgs/alipay.png" />
</div>

##### Over

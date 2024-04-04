# 网页存档 Archive Api

[English](./README.en.md)

这是一个网页存档项目，通过 selenium 模拟访问的方式，以图片和 PDF 格式保存你认为互联网上可能会在不久后消失的资源。

## Demo

https://archive.qdzx.icu/

## 帮助我们适配更多网站

在 [crawl/optimize_config.py](https://github.com/yxzlwz/archive-api/blob/main/crawl/optimize_config.py) 中，你可以通过网站的域名和路径为不同站点设置一些爬取优化项，例如关闭知乎提示登录的弹窗等。

目前我们支持如下操作：

- 点击（click）：提供页面元素的 Selector 信息，在页面加载完成后
- 等待（wait）：提供等待时间，应对浏览器无法识别的延迟加载

关于懒加载的适配，可在存档网页时选择是否开启。若开启该功能，页面将模拟访问者从头滚动到尾（自然也带来）。需要注意的是，如果你的设备所处的网络环境较差，可能在开启懒加载适配后仍有图片不能完成加载，你可以改善网络环境或修改懒加载每次滚动后的等待时长。

## 部署教程

### 后端

[Debian/Ubuntu 安装 Chrome 和 Chrome Driver 并使用 selenium 自动化测试](https://www.yixiangzhilv.com/blogs/20230709165453.html)

本项目需要 Redis 和 RabbitMQ。此外只需要根据标准的 Django 项目启动方式配置即可。

### 前端

https://github.com/yxzlwz/archive-frontend

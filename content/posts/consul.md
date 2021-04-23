---
title: "Python利用Consul实现服务发现"
date: 2021-04-23T14:17:25+08:00
draft: false
toc: false
images:
tags: 
  - consul
  - 服务发现
  - 微服务
---



# 1.背景

由于基金筛选系统和组合管理系统间存在一些互相需要使用到的基础数据，但又不想重复创建数据库表单和同步数据，因此在两个项目中使用了grpc来实现数据调用；早期实现的grpc版本中直接使用对方的IP和端口，每次调整或部署到其他地方都需要修改代码，因此考虑使用服务注册和发现来解决这个问题。

对比了**etcd**和**consul**两个方案，由于后端使用的语言是python，而etcd的版本比较多，导致相关的库也需要对应版本，使用起来比较麻烦，因此最终使用consul和对应的库`python-consul`。



# 2.安装与启动

## 2.1安装

直接前往 [Consul by HashiCorp](https://www.consul.io/) 官网下载对应系统的可执行文件即可，以Linux为例

```bash
$ cd  /home/downloads
$ mkdir consul && cd consul
$ wget https://releases.hashicorp.com/consul/1.9.5/consul_1.9.5_linux_amd64.zip
$ unzip consul_1.9.5_linux_amd64.zip
```



## 2.2启动

以刚刚下载的文件为例：

```bash
$ ./consul agent -server -bootstrap-expect 1 -data-dir=/tmp/consul -node=n1 -bind=127.0.0.1 -client=0.0.0.0 -ui
```

默认使用端口`8500`，在浏览器中输入服务器`{ip}:8500`即可通过web查看注册的服务了，当然目前只有一个默认的健康检测服务。

![启动页面](/images/consul-start.png)



# 3.在Python中使用

首先需要安装`python-consul`库：

```bash
$ pip3 install python-consul
```

简单示例：

```python
#test.py
import consul


class Consul(object):

    def __init__(self, host='10.170.139.10', port=8500):
        self._consul = consul.Consul(host, port)

    def register(self, name, host, port):
        """注册服务"""
        self._consul.agent.service.register(
            name=name, service_id=name, address=host, port=port,
            check=consul.Check().tcp(host=host, port=port, interval='5s',
                                     timeout='30s', deregister='30s')
        )

    def find(self, name):
        """发现服务"""
        services = self._consul.agent.services()
        server = services.get(name)
        if not server:
            return None, False
        addr = server['Address']
        port = server['Port']
        return (addr, port), True


if __name__ == '__main__':
    c = Consul()
    c.register('fund_filter_django', '10.170.139.10', 50051)
    print(c.find('fund_filter_django'))

```

执行文件可以看到：

```bash
$ python3 test.py
(('10.170.139.10', 50051), True)
```

查看web页面可以看到：

![注册服务](/images/consul-register.png)
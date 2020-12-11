---
title: "Python中使用UDP来推送数据"
date: 2020-12-11T16:41:32+08:00
draft: false
toc: false
images:
tags: 
  - python
  - udp
---

## 1.UDP简介

UDP协议（User Datagram Protocol）中文名称是用户数据报协议，是OSI（Open System Interconnection，开放式系统互联）参考模型中一种无连接的传输层协议，不需要建立连接就能直接进行数据发送和接收，属于不可靠的、没有时序的通信，但是UDP协议的实时性比较好，通常用于视频直播相关领域。

使用UDP推送数据时，不会考虑客户端是否会接受到数据，因此并不能保证它们能到达目的地。但由于UDP在传输数据报前不用在客户和服务器之间建立一个连接，且没有超时重发等机制，故而传输速度很快。

接下来简单写个demo来尝试写一个推送服务。

## 2.服务端

服务端代码如下

```python
# server.py
import socket
import time
import datetime

from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(2)


class Manager(object):
    """客户端管理
    """
    _clients = {}
    server: socket.socket

    def __init__(self, address: str, port: int):
        """Manager instance

        Args:
            address: 地址
            port: 端口
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (address, port)
        server_socket.bind(address)
        self.server = server_socket

    def register(self, name, client):
        """注册客户端

        Args:
            name: 客户端名称
            client: 客户端ip
        """
        self._clients.update({name: client})
        print(f'用户 {name} 成功注册')

    def unregister(self, name: str):
        """取消注册

        Args:
            name: 客户端名称
        """
        if name in self._clients.keys():
            self._clients.pop(name)

    def broadcast(self, msg: str):
        """为每一个注册的客户端推送消息

        Args:
            msg: 消息内容
        """
        for client in self._clients.values():
            self.server.sendto(msg.encode(), client)

    def check_register(self):
        """监听注册事件"""
        while True:
            name, client_address = self.server.recvfrom(1024)
            if name:
                self.register(name.decode(), client_address)

    def do(self):
        """模拟推送业务"""
        while True:
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.broadcast(date)
            time.sleep(10)

    @staticmethod
    def serve(address, port):
        manager = Manager(address, port)
        pool.submit(manager.check_register)
        pool.submit(manager.do)


if __name__ == '__main__':
    Manager.serve('0.0.0.0', 9000)

```

server端每隔10秒会向订阅的客户端推送一次数据，数据内容用当前时间模拟。发现订阅和推送数据放入线程池中处理，避免堵塞。

## 3.客户端

```py
# client.py
import socket
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(5)


class Client(object):
    """客户端"""

    _server: socket.socket
    _address: tuple

    def __init__(self, name, address, port):
        self.name = name
        self._address = (address, port)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def register(self):
        self._server.sendto(self.name.encode(), self._address)

    def receive(self):
        while True:
            receive, sender = self._server.recvfrom(1024)
            receive = receive.decode()
            print(f'{self.name} 收到数据 {receive}')


if __name__ == '__main__':
    addr = '127.0.0.1'
    p = 9000
    users = ['A', 'B', 'C', 'D', 'E']

    # 模拟5个用户去订阅数据
    for user in users:
        client = Client(user, addr, p)
        client.register()
        pool.submit(client.receive)

```

客户端模拟5个用户去订阅数据，订阅后会持续收到服务端推送的数据。取消注册的方法暂未实现，原理类似。


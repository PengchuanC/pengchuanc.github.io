import socket
import time
import datetime

from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(2)


class Manager(object):
    """客户端管理

    Attributes:
        address: 地址
        port: 端口
    """
    _clients = {}
    server: socket.socket

    def __init__(self, address: str, port: int):
        """Inits manager"""
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

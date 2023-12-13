import socket
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(5)


class Client(object):
    """客户端

    Attributes:
        name: 用于注册的唯一标识，通常使用uuid
        address: 远程服务器地址
        port: 远程服务器端口
    """

    _server: socket.socket
    _address: tuple

    def __init__(self, name, address, port):
        """Inits client"""
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

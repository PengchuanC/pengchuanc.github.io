import grpc

from pathlib import Path

from file_server import fileserver_pb2 as fp, fileserver_pb2_grpc as fpg


base_path = Path(__file__).parent


def send_file():
    """上传文件

    模拟大文件，分块发送
    Returns:

    """
    file_path = base_path / 'download' / 'download.docx'
    # 模拟大文件，分块读取发送
    size = 1024
    with open(file_path, 'rb') as f:
        start = 0
        while True:
            f.seek(start)
            read = f.read(size)
            if not read:
                return
            request = fp.RequestSend(data=read)
            yield request
            start += size


class Client(object):
    stub: fpg.FileTransferStub = None

    def __init__(self, port=50051):
        self.channel = grpc.insecure_channel(f'127.0.0.1:{port}')

    def connect(self):
        self.stub = fpg.FileTransferStub(self.channel)

    def close(self):
        self.channel.close()

    def download(self, name: str = 'send.xlsx'):
        """文件下载

        会将send.xlsx文件下载到 ./file_sever/download目录
        Args:
            name: 下载文件名，默认为 send.xlsx

        Returns:

        """
        r = fp.RequestFile(name=name)
        response = self.stub.DownloadFile(r)
        download = base_path / 'download' / name
        with open(download, 'wb') as f:
            for r in response:
                f.write(r.data)

    def send(self):
        """上传文件

        默认将上传 ./file_server/download/download.docx
        Returns:

        """
        file = send_file()
        resp = self.stub.SendFile(file)
        return resp

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    import time
    with Client() as client:
        # 上传文件
        resp_status = client.send()
        print(resp_status)

        # 下载文件
        a = time.time()
        client.download('send.pptx')
        b = time.time()
        print(round(b-a, 6))

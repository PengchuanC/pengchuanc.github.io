import time

import grpc
from concurrent import futures
from pathlib import Path

import file_server.fileserver_pb2 as fp
import file_server.fileserver_pb2_grpc as fpg


base_path = Path(__file__).parent


def file_read(name: str):
    """读取待发送的文件的内容

    由于是测试脚本，直接读取待下载的文件，即 ./file_server/send.xlsx
    模拟大文件需要分块读取，持续发送
    Args:
        name: 文件名
    Returns:

    """
    send_file_path = base_path / 'send' / name
    size = 1024*1024*2
    with open(send_file_path, 'rb') as file:
        start = 0
        while True:
            file.seek(start)
            read = file.read(size)
            if not read:
                return
            yield fp.ResponseStream(data=read)
            start += size


class FileTransferServer(fpg.FileTransferServicer):
    """文件传输服务"""

    def SendFile(self, request_iterator, context):
        """文件发送服务

        继承定义好的文件发送服务
        Args:
            request_iterator: 上传的文件流 : Generator[byte]
            context: 上下文

        Returns:
            文件上传的状态 :ResponseStatus
        """
        print('接受到文件上传请求')
        send_file = base_path / 'send' / 'download.docx'
        try:
            with open(send_file, 'wb') as f:
                for r in request_iterator:
                    f.write(r.data)
            return fp.ResponseStatus(ok=True)
        except Exception as e:
            print(e)
            return fp.ResponseStatus(ok=False)

    def DownloadFile(self, request, context):
        """文件下载服务

        继承定义好的文件下载服务
        Args:
            request: 请求需要下载的文件名 :RequestFile
            context: 上下文管理

        Returns:
            文件下载的数据流 :ResponseStream
        """
        print(request.name)
        file_name = request.name
        file = file_read(name=file_name)
        for response in file:
            yield response

    @staticmethod
    def serve():
        """启动服务

        Returns:

        """
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        fpg.add_FileTransferServicer_to_server(FileTransferServer(), server)
        server.add_insecure_port("[::]:50051")
        server.start()
        try:
            while True:
                print("start server")
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    FileTransferServer.serve()

import random
import queue
from multiprocessing.managers import BaseManager


# 全局变量，存放产生的数据
products = queue.Queue()


def task_queue():
    """获取任务队列

    用于注册到BaseManager的任务队列
    Returns:
        queue.Queue: 获取进程安全的任务队列

    """
    return products


def close():
    print('收到请求，结束进程')
    exit()


if __name__ == '__main__':
    BaseManager.register('task_queue', task_queue)
    BaseManager.register('close', close)
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.start()
    tasks = manager.task_queue()
    while True:
        continue


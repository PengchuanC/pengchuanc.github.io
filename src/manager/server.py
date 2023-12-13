import random
import time
from multiprocessing.managers import BaseManager


def producer():
    """模拟生产者，生产数据

    Returns:
        int: 将产生的随机数当作产品

    """
    p = random.randint(1, 10)
    return p


if __name__ == '__main__':
    BaseManager.register('task_queue')
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.connect()
    tasks = manager.task_queue()
    while True:
        tasks.put(producer())
        time.sleep(2)


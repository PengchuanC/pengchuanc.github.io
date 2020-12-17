from multiprocessing.managers import BaseManager


if __name__ == '__main__':
    BaseManager.register('task_queue')
    BaseManager.register('close')
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.connect()
    tasks = manager.task_queue()
    while True:
        if tasks.empty():
            manager.close()
        print(tasks.get())

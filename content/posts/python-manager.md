---
title: "Python利用Manager在分布式进程间进行通信"
date: 2020-12-17T11:01:25+08:00
draft: false
toc: false
images:
tags: 
  - python
  - manager
  - 分布式
  - 多进程通信
---

在具有亲缘的多进程程序中，通常可用使用`queue`、`pipe`等数据结构来进行数据共享和传递消息，但在分布式进程中，进程间的通信还需要依靠网络来进行传输。

在之前的文章中，我们通过grpc服务来传输数据，实际上在Python标准库`multiprocessing`的`managers`模块已经包含了分布式进程通信的功能，主要使用`BaseManager`对象。

## 1.BaseManager对象

官网文档对BaseManager的描述：

```py
class multiprocessing.managers.BaseManager([address[, authkey]])
	"""
	创建一个 BaseManager 对象。
	一旦创建，应该及时调用 start() 或者 get_server().serve_forever() 以确保管理器对象对应的管理进程已经启动。

	address 是管理器服务进程监听的地址。如果 address 是 None ,则允许和任意主机的请求建立连接。

	authkey 是认证标识，用于检查连接服务进程的请求合法性。如果 authkey 是 None, 则会使用 current_process().authkey , 否则，就使用 authkey , 需要保证它必须是 byte 类型的字符串。

	start([initializer[, initargs]])
		为管理器开启一个子进程，如果 initializer 不是 None , 子进程在启动时将会调用initializer(*initargs) 。

    get_server()
    	返回一个 Server对象，它是管理器在后台控制的真实的服务。 Server对象拥有serve_forever() 方法。

        >>>
        >>> from multiprocessing.managers import BaseManager
        >>> manager = BaseManager(address=('', 50000), authkey=b'abc')
        >>> server = manager.get_server()
        >>> server.serve_forever()
        Server 额外拥有一个 address 属性。

    connect()
    	将本地管理器对象连接到一个远程管理器进程:

        >>>
        >>> from multiprocessing.managers import BaseManager
        >>> m = BaseManager(address=('127.0.0.1', 50000), authkey=b'abc')
        >>> m.connect()
        
    shutdown()
        停止管理器的进程。这个方法只能用于已经使用 start() 启动的服务进程。

        它可以被多次调用。

    register(typeid[, callable[, proxytype[, exposed[, method_to_typeid[, create_method]]]]])
    	一个 classmethod，可以将一个类型或者可调用对象注册到管理器类。

    	typeid 是一种 "类型标识符"，用于唯一表示某种共享对象类型，必须是一个字符串。

        callable 是一个用来为此类型标识符创建对象的可调用对象。如果一个管理器实例将使用 connect() 方法连接到服务器，或者 create_method 参数为 False，那么这里可留下 None。

        proxytype 是 BaseProxy  的子类，可以根据 typeid 为共享对象创建一个代理，如果是 None , 则会自动创建一个代理类。

        exposed 是一个函数名组成的序列，用来指明只有这些方法可以使用 BaseProxy._callmethod() 代理。(如果 exposed 是 None, 则会在 proxytype._exposed_ 存在的情况下转而使用它) 当暴露的方法列表没有指定的时候，共享对象的所有 “公共方法” 都会被代理。（这里的“公共方法”是指所有拥有 __call__() 方法并且不是以 '_' 开头的属性）

        method_to_typeid 是一个映射，用来指定那些应该返回代理对象的暴露方法所返回的类型。（如果 method_to_typeid 是 None, 则 proxytype._method_to_typeid_ 会在存在的情况下被使用）如果方法名称不在这个映射中或者映射是 None ,则方法返回的对象会是一个值拷贝。

        create_method 指明，是否要创建一个以 typeid 命名并返回一个代理对象的方法，这个函数会被服务进程用于创建共享对象，默认为 True 。

    BaseManager 实例也有一个只读属性。

    address
    	管理器所用的地址。
    """
```

接下来尝试使用`BaseManager`来进行分布式进程间的通信，由于是在本机多个`cmd`窗口下模拟分布式，故ip地址均使用`127.0.0.1:5000`。

## 2.Server端

代码如下：

```py
# server.py
import random
import queue
import time
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


def producer():
    """模拟生产者，生产数据

    Returns:
        int: 将产生的随机数当作产品

    """
    p = random.randint(1, 10)
    return p


if __name__ == '__main__':
    BaseManager.register('task_queue', task_queue)
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.start()
    tasks = manager.task_queue()
    while True:
        tasks.put(producer())
        time.sleep(2)

```

首先创建一个全局的`queue`来存放数据(注意`queue`的特点是先进先出(FIFO)，当从一个空的`queue`获取数据时会发生堵塞)，模拟实际业务中产生的数据的容器，如存放爬虫获取到的媒体文件的url，供其他进程获取。

然后为创建的数据容器提供一个获取方法，然后注册到`BaseManager`，注册后其他进程便可以注册相同的名字来获取到这个方法，然后获取到数据容器。

在服务端实例化`BaseManager`对象，传入服务器地址，并调用`start`对象开启服务。

最后在循环事件中模拟生产过程。

## 3.Client端

client端模拟消费过程，代码如下：

```py
# client.py
from multiprocessing.managers import BaseManager


if __name__ == '__main__':
    BaseManager.register('task_queue')
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.connect()
    tasks = manager.task_queue()
    while True:
        print(tasks.get())

```

这样便实现了分布式进程间的通信和数据共享。

## 4.进一步拆分

在实际业务中，可能会有多个生产者和多个消费者，这种情况下需要把负责通信的模块剥离出来，只作为通信的管理部分，即生产者向管理者写入数据，消费者从管理者读取数据。

### 4.1 Manager

```py
# manager.py
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

```

### 4.2 Server

```python
# server.py
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

```

### 4.3 Client

```py
# client.py
from multiprocessing.managers import BaseManager


if __name__ == '__main__':
    BaseManager.register('task_queue')
    manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'producer')
    manager.connect()
    tasks = manager.task_queue()
    while True:
        print(tasks.get())

```

这样`Manager`便可以只用于管理通信，与业务剥离。
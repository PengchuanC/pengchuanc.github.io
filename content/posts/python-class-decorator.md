---
title: "Python使用装饰器来实现重试"
date: 2020-12-15T10:09:06+08:00
draft: false
toc: false
images:
tags: 
  - python
  - retry
  - 装饰器类
---

在之前使用grpc的项目中偶尔会遇到连接时间过久，tcp连接断掉的情况，于是尝试写一个装饰器来实现自动重连3次，即最大尝试4次连接。

主要使用了python中class的魔术方法`__call__`和递归函数。

## 1.Python中的`__call__`方法

`__call__`函数的作用是将一个类变为`callable`对象，即可用用`()`来调用一个已经实例化的对象，这也是将`class`作为装饰器的关键。

```python
class Test(object):
    def __init__(self):
        print('调用init')

    def __new__(cls, *args, **kwargs):
        print('调用new')
        return object.__new__(cls)

    def __call__(self, *args, **kwargs):
        print('调用call')
```

python中对象实例化时，会一次调用`__new__`和`__init__`函数，然后调用实例化后的对象，会调用`__call__`函数，比如：

```pow
>>> t = Test()
调用new
调用init

>> t()
调用call
```

## 2.实现装饰器

了解`__call__`运行的机制后，便可以利用它的特性来实现装饰器了。

```py
class Reconnect(object):
    """网络访问自动重连

    Attributes:
        func: 被装饰的函数
        calls: 函数被调用的次数
    """

    def __init__(self, func):
        self.func = func
        self.calls = 0

    def reconnect(self, *args, **kwargs):
        """重新连接

        当次数达到第四次时，直接返回函数，不论是否成功，不再进行重连
        当次数小于四次时，如果是ConnectionError则递归调用重连函数
        如果是其他错误，则直接抛出错误
        """
        self.calls += 1
        if self.calls > 3:
            return self.func(*args, **kwargs)
        try:
            return self.func(*args, **kwargs)
        except ConnectionError as e:
            print(e)
            return self.reconnect(*args, **kwargs)
        except Exception as e:
            raise e

    def __repr__(self):
        """尝试还原函数本身签名"""
        return repr(self.func)

    def __call__(self, *args, **kwargs):
        return self.reconnect(*args, **kwargs)

```

初始化装饰器时，会需要传入一个被装饰的函数和生成一个内部用来记录重试次数的变量`calls`，重试的逻辑主要在`reconnect`函数中实现，重试逻辑中只捕获`ConnectionError`并进行重试，接下来模拟网络连接中会发生的错误。

## 3.模拟网络访问中的错误

```
@Reconnect
def add(a, b):
    # 模拟不稳定的网络
    net_state = random.randint(0, 10)
    if net_state > 9:
        raise ConnectionRefusedError(f'connection refuse, net state {net_state}')
    elif net_state > 5:
        raise ConnectionError(f'connection error, net state {net_state}')
    return a+b
```

利用`random`库产生的随机数来模拟网络环境，调用`add`检验装饰器是否生效：

```pow
>>> add(5, 2)
7

>>> add(5, 2)
connection error, net state 6
connection error, net state 8
connection refuse, net state 10
7
```

可用看到，装饰器已经生效。

## 4.关于函数签名

在定义装饰器时，使用到了`__repr__`方法，该方法主要定义对象的输出内容，当函数经过装饰器的装饰，其实际签名信息已经被覆盖，在日志中已经无法定位到具体函数的信息，如果在上例中，注释掉`__repr__`相关内容，我们可以看到：

```
>>> add
<Reconnect object at 0x000001A80CE48FD0>
```

实际上`add`函数自身信息已经丢失，如果使用了`__repr__`后，则可用看到：

```
>>> add
<function add at 0x0000021862BAE040>
```

在函数型装饰器中，可用使用`collections`模块下的`wraps`对象来实现函数的反签名，在装饰器类中尚未尝试，可以作为后续研究内容。

## 5.完整代码

```py
# demo.py
import random


class Reconnect(object):
    """网络访问自动重连

    Attributes:
        func: 被装饰的函数
        calls: 函数被调用的次数
    """

    def __init__(self, func):
        self.func = func
        self.calls = 0

    def reconnect(self, *args, **kwargs):
        """重新连接

        当次数达到第四次时，直接返回函数，不论是否成功，不再进行重连
        当次数小于四次时，如果是ConnectionError则递归调用重连函数
        如果是其他错误，则直接抛出错误
        """
        self.calls += 1
        if self.calls > 3:
            return self.func(*args, **kwargs)
        try:
            return self.func(*args, **kwargs)
        except ConnectionError as e:
            print(e)
            return self.reconnect(*args, **kwargs)
        except Exception as e:
            raise e

    def __repr__(self):
        """尝试还原函数本身签名"""
        return repr(self.func)

    def __call__(self, *args, **kwargs):
        return self.reconnect(*args, **kwargs)


@Reconnect
def add(a, b):
    # 模拟不稳定的网络
    net_state = random.randint(0, 10)
    if net_state > 9:
        raise ConnectionRefusedError(f'connection refuse, net state {net_state}')
    elif net_state > 5:
        raise ConnectionError(f'connection error, net state {net_state}')
    return a+b


def minus(a, b):
    return a-b


if __name__ == '__main__':
    print(add)
    print(minus)
    print(add(5, 2))

```


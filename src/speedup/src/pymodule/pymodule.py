

def hello(name):
    return "Hello, %s !" % name


def fibnacci(n):
    if n < 2:
        return n
    else:
        return fibnacci(n - 1) + fibnacci(n - 2)


cpdef str hello(str name) except *:
    return "hello, " + name

cdef int fib(int n):
    if n <= 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

cpdef int fibnacci(int n) except *:
    return fib(n)

import cProfile

from speedup import pp
from speedup import cp
from speedup import cy
from speedup import cc
from speedup import py


RUN_TIMES = 35

def test_pp():
    """pure python"""
    for i in range(RUN_TIMES):
        pp.fibnacci(i)


def test_py():
    """compiled pure python"""
    for i in range(RUN_TIMES):
        py.fibnacci(i)


def test_cp():
    """c extension"""
    for i in range(RUN_TIMES):
        cp.fibnacci(i)

def test_cy():
    """cython extension"""
    for i in range(RUN_TIMES):
        cy.fibnacci(i)

def test_cc():
    """cpp extension"""
    for i in range(RUN_TIMES):
        cc.fibnacci(i)


if __name__ == "__main__":
    print("pure python: ")
    cProfile.run("test_py()")
    print("compiled python: ")
    cProfile.run("test_py()")
    print("c extension: ")
    cProfile.run("test_cp()")
    print("cpp extension: ")
    cProfile.run("test_cc()")
    print("cython extension: ")
    cProfile.run("test_cy()")

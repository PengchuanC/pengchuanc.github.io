import cProfile

from speedup import pp
from speedup import cp
from speedup import cy
from speedup import cc
from speedup import py


RUN_TIMES = 10000
NAME = "World"

def test_pp():
    """pure python"""
    for _ in range(RUN_TIMES):
        pp.hello(NAME)


def test_py():
    """compiled pure python"""
    for _ in range(RUN_TIMES):
        py.hello(NAME)


def test_cp():
    """c extension"""
    for _ in range(RUN_TIMES):
        cp.hello(NAME)

def test_cy():
    """cython extension"""
    for _ in range(RUN_TIMES):
        cy.hello(NAME)

def test_cc():
    """cpp extension"""
    for _ in range(RUN_TIMES):
        cc.hello(NAME)


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

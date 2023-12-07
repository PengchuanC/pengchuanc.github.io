---
title: python extension
date: 2023-12-07 19:04:22+8:00
tags: 
  - python
  - cpp
  - c
  - cython
---


# 1. 简介

Python 语言的扩展模块，主要是用 C 语言编写的，可以直接在 Python 中使用。但实际上除了C语言的扩展模块，Python 还支持其他语言的扩展模块，比如 C++、Cython、C#、Rust 等，实现的方式有ABI、CFFI、SWIG等。

此次主要研究 Python 的 C 系列扩展模块，基本都是通过ABI的方式实现，包括C、Cython和CPP(pybind11)，作为对比，会加入纯Python和Python代码编译成动态链接库来作为对比项。
使用的Python解释器为官方的CPython解释器，版本为3.11.6，Cython为3.0以上版本，使用的编译工具为MSVC，如果要编译源码，必须提前安装[Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)。

# 2. 扩展模块的类型

windows下，Python的扩展模块通常是由其他语言编译出的动态链接库，可以直接在 Python 中使用，在本次的测试环境中文件名通常为`modulename.cp311-win_amd64.pyd`。

本次测试主要测试两类场景:

- 1. 需要频繁在语言间进行数据交换，但是CPU开销很小的场景
- 2. 语言间通信次数很少，但是CPU开销较大的场景

# 3. 代码编写

本次测试要实现的功能很简单，主要包含`hello(name)`和`fibnacci(n)`两个函数，来对应前述两种场景。

## 3.1 纯Python

```python

def hello(name):
    return "Hello, %s !" % name


def fibnacci(n):
    if n < 2:
        return n
    else:
        return fibnacci(n - 1) + fibnacci(n - 2)

```

## 3.2 C

C语言扩展模块基于官方标准的Python/C API开发。

```c
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "stdio.h"

static PyObject *Py_hello(PyObject *self, PyObject *args)
{
    const char *name;

    if (!PyArg_ParseTuple(args, "s", &name))
    {
        return NULL;
    }

    char greeting[50];
    snprintf(greeting, sizeof(greeting), "Hello, %s!", name);
    return Py_BuildValue("s", greeting);
}

long long fibonacci(int n)
{
    if (n <= 2)
    {
        return 0;
    }
    else
    {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

static PyObject *Py_fibnacci(PyObject *self, PyObject *args)
{
    int n;

    if (!PyArg_ParseTuple(args, "i", &n))
    {
        return NULL;
    }

    long long ret = fibonacci(n);

    return Py_BuildValue("i", ret);
}

static PyMethodDef methods[] = {
    {"hello", Py_hello, METH_VARARGS, "Print Hello, World!"},
    {"fibnacci", Py_fibnacci, METH_VARARGS, "cal fibnacci"},
    {NULL, NULL, 0, NULL} // 结束标志
};

static struct PyModuleDef cpmodule = {
    PyModuleDef_HEAD_INIT,
    "cp",      /* name of module */
    "cp desc", /* module documentation, may be NULL */
    -1,
    methods};

PyMODINIT_FUNC PyInit_cp(void)
{
    return PyModule_Create(&cpmodule);
}
```

## 3.3 Cython

```python
cpdef str hello(str name) except *:
    return "hello, " + name


cdef int fib(int n):
    if n <= 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


cpdef int fibnacci(int n) except *:
    return fib(n)

```

## 3.4 CPP

CPP版本使用[pybind11](https://pybind11.readthedocs.io/en/stable/)来实现语言绑定。

```cpp
#include <string>
#include <pybind11/pybind11.h>

namespace py = pybind11;

py::str hello(py::str name)
{
    py::str greeting = py::str("hello, {} !").format(name);
    return greeting;
}

long long fibnacci(long long n)
{
    if (n < 2)
        return n;
    return fibnacci(n - 1) + fibnacci(n - 2);
}

PYBIND11_MODULE(cc, m)
{
    m.doc() = "ccmodule";
    m.def("hello", &hello, "Say hello");
    m.def("fibnacci", &fibnacci, "Fibonacci");
}
```

# 4. 项目构建

本次项目使用setuptools进行构建，编译扩展的脚本在`setupo.py`中，将各个语言的扩展作为子模块放到`speedup`项目下。

# 4.1 目录结构

```
speedup
├── src
│   ├── ccmodule          // cpp扩展
│   │   └── ccmodule.cc
│   ├── cpmodule          // c扩展
│   │   └── cpmodule.c
│   ├── cymodule          // cython扩展
│   │   ├── cymodule.pxd
│   │   └── cymodule.pyx
│   ├── pymodule          // 纯python编译
│   │   └── pymodule.py
│   └── speedup
│       ├── __init__.py
│       └── pp.py         // 纯python
├── tests
│   ├── test_hello.py
│   └── test_fibnacci.py
├── README.md
├── pyproject.toml        // 项目描述
└── setup.py              //  构建脚本
```

# 4.2 构建

## 4.2.1 pyproject.toml

```toml
[build-system]
requires = ["setuptools", "Cython", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "speedup"
version = "0.0.1"

[tool.setuptools]
package-dir = { "" = "src" }
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
speedup = ["*.pyi", "*.pxd"]
"speedup.cp" = ["*.pxd", "*.pyi", "*.pyx"]
"speedup.cy" = ["*.pxd", "*.pyi", "*.pyx"]

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
pythonpath = "src"
```

## 4.2.2 setup.py

```python
from setuptools import Extension, setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

setup(
    ext_modules=[
        Extension("speedup.cp", ["src/cpmodule/cpmodule.c"]),
        Pybind11Extension("speedup.cc", ["src/ccmodule/ccmodule.cc"]),
        Extension("speedup.cy", ["src/cymodule/cymodule.pyx"]),
        Extension("speedup.py", ["src/pymodule/pymodule.py"]),
    ],
    build_ext=build_ext
)
```

## 4.2.3 编译

```bash
> pip install -U build wheel cython setuptools pybind11  #  安装依赖
> python -m build -n  # 编译和构建whl包
> pip install dist/speedup-0.0.1-cp311-cp311-win_amd64.whl  # 安装
```

# 5. 性能测试

使用cProfile进行性能测试，测试单位为秒，测试命令如下：

```bash
> python tests/test_hello.py
> python tests/test_fibnacci.py
```

## 5.1 测试结果

| situation | Python | Python Compiled | C     | Cython | CPP   |
| --------- | ------ | --------------- | ----- | ------ | ----- |
| hello     | 0.001  | 0.001           | 0.003 | 0.001  | 0.011 |
| fibnacci  | 0.909  | 0.900           | 0.033 | 0.045  | 0.051 |

## 5.2 分析

从测试结果可以看出：

在场景1，Python/Cython的性能会优于C/CPP，在语言间通信较多且任务十分简单时，不适合编写C扩展；在情景2下，C API性能明显强于其它扩展，Cython性能稍弱，Pybind11是对CPP和C API的封装，性能也不错，但开销还是比C/Cython高，
原生Python最高。

- 纯Python的性能优于C/Cython/CPP，主要是因为跨语言对对象进行序列化/反序列化的开销较大；
- 在性能需求较高时，C扩展的速度是最快的，但考虑到C的开发维护成本，Cython/CPP也是不错的选择；
- 对比C，CPP(pybind11)作为C的高级封装和扩展，性能稍弱一点；
- 对比C，Cython在不同情形下和C互有优劣；
- 对比Python，Cython会有性能提升；

# 6. 源码分享

[speedup](https://github.com/PengchuanC/pengchuanc.github.io/tree/main/src/speedup)

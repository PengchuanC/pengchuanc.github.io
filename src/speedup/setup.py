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

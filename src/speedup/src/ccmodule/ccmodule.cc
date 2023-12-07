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
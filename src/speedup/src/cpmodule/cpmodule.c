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

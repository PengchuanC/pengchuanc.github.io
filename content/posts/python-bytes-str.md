---
title: "Python中的str类型和int数组类型转换"
date: 2020-12-10T09:42:59+08:00
draft: false
toc: false
images:
tags: 
  - python
  - bytes
---

在编程语言中，string类型往往是通过int数组来实现的，在python中，str和int[]同样可以转换

### 1.str转bytes

将字符串转化为bytes类型，即int数组

```pow
>>> a = 'abc'

>>> # 将a转为bytes类型
>>> a.encode()
b'abc'

>>> # 转为List[int]
>>> [x for x in a.encode()]
[97, 98, 99]
```

### 2.将int数组转化为str

```po
>>> a = [97, 98, 99]

>>> # 先转为bytes
>>> bytes(a)
b'abc'
>>> bytes(a).decode()
'abc'
```


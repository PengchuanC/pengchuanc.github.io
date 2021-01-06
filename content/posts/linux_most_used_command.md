---
title: "常用Linux命令"
date: 2021-01-06T15:22:11+08:00
draft: false
toc: false
images:
tags: 
  - Linux
---

# 任务中止

## 1.中止多进程任务

假设任务名为 `qcluster`

![image-20210106152455606](/images/linux-ps.png)

```sh
ps aux|grep qcluster|grep -v grep|cut -c 9-15|xargs kill -9
```


---
title: "Mariadb(MySQL)初始配置"
date: 2021-02-04T17:05:55+08:00
draft: false
toc: false
images:
tags: 
  - MariaDB
  - MySQL
---



数据库各项配置主要在`/etc/my.cnf`文件中修改。



# 1.数据库存放位置

安装完MariaDB后，数据资源一般默认存放在`/var/lib/mysql`目录下，该目录空间一般不大，可修改`datadir`项目来更改数据保存位置，对于开启**SELinux**的发行版来说，修改数据保存位置可能导致数据库启动失败，可以通过`setenforce 0`来关闭SELinux。

一般建议移动整个`/var/lib/mysql`目录，如果这样操作，记得修改`socket`条目的位置。

```plain
# 初始配置
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# 修改后
datadir=/root/mysql
socket=/root/mysql/mysql.sock
```

# 2.影响到数据库超时的设置

```cnf
# 服务器关闭非交互连接之前等待活动的秒数
wait_timeout=28800

# 服务器关闭交互式连接之前等待活动的秒数
interactive_timeout=28800
```

# 3.缓冲区大小

```cnf
# 索引的缓冲区大小，增加它可得到更好的索引处理性能
key_buffer_size=256M

# 单次连接最大数据量
max_allowed_packet=768M

# 排序、读查询、join操作所能使用的缓冲区大小，每一个连接独享
read_buffer_size=4M
sort_buffer_size=4M
join_buffer_size=8M
```

# 4.连接数量管理

```cnf
# 最大连接进程数
max_connections=768
max_connect_errors=1000
```


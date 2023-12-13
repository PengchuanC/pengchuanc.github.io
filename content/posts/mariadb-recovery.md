---
title: "Mariadb意外崩溃数据恢复"
date: 2021-09-03T11:05:55+08:00
draft: false
tags:
  - mariadb
  - mysql
  - 数据恢复
---



# 1.事故还原

优于同时在多个终端执行select、insert和delete操作，数据库意外崩溃



# 2.数据恢复

## 2.1 尝试重新启动

执行`service mysqld restart`发现数据库报错，无法启动

## 2.2 进入恢复模式

当发现数据无法启动后，尝试进入恢复模式，`vi /etc/my.cnf`

在配置文件中[mysqld]部分增加以下内容

```cnf
[mysqld]
innodb_force_recovery=1
innodb_purge_thread=0
```

然后执行`service mysqld restart`重启数据库，如果继续失败则将`innodb_force_recovery`的值修改为2，其中`innodb_force_recovery`分为0-6这七个等级，可用逐个尝试，直至数据重新启动

## 2.3 备份数据

使用 `mysqldump`备份数据库

以我的情况为例

```sh
> mysqldump -uroot -p --databases am_sma_third > /home/sma/backup/am_sma_third_20210903.sql
```

## 2.4 初始化数据库

初始化之前，为防止意外，将旧的数据库文件备份一下，文件位置可以从配置文件`my.cnf`查看

```cnf
[mysqld]
datadir=/home/mysql/datadir
socket=/home/mysql/datadir/mysql.sock
```

其中datadir便是文件位置，进行备份

```sh
> cd /home/mysql
> mkdir datadirbak && mkdir datadirbak/20210903
> mv datadir/* datadirbak/20210903/
```

备份完成后，初始化数据库

```sh
> mysql_install_db --user=mysql --basedir=/usr --datadir=/home/mysql/datadir/
```

对文件夹重新授权，防止意外

```sh
> chown -R mysql:mysql /home/mysql 
```

注释掉恢复模式

```cnf
[mysqld]
# innodb_force_recovery=1
# innodb_purge_thread=0
```

重启数据库

```
> service mysqld restart
```

## 2.5 恢复数据

登陆到数据库

```sh
> mysql -uroot -p
```

利用`source`命令恢复数据，以我的**sm_sma_third**库为例

```mysql
mysql> create database sm_sma_third;
mysql> source /home/sma/backup/sm_sma_third_20210903.sql
```

等待恢复完成，重新对用户进行授权即可。
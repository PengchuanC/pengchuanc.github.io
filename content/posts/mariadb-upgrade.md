---
title: "MariaDB 升级后无法运行"
date: 2021-02-24T10:15:21+08:00
draft: false
toc: false
images:
tags: 
  - MariaDB升级报错
  - MySQL
---

# 1.事情起因

在redhat每次执行完`yun update`后，MariaDB也会升级，但我之前更换过MariaDB的数据存储目录，将数据保存在了`/home/mysql`目录下，导致每次升级完MariaDB后，无法启动server。

# 2.解决方案

## 2.1 更换目录

更换目录后，需要对目录重新授权，因为默认情况下，MariaDB的用户和用户组为`mysql:mysql`，授权代码为：

```sh
~ chown -R mysql:mysql /home/mysql
~ chown 775 /home/mysql
```

## 2.2 关闭selinux

通过一下命令可以临时关闭selinux：

```sh
~ setenforce 0
```

要永久禁用selinux，可以使用文本编辑器打开`/etc/sysconfig/selinux`文件，如下所示：

```sh
~ vi /etc/sysconfig/selinux
```

然后将配置selinux=enforcing改为selinux=disabled，如下图所示。

```plain
SELINUX=disabled
```

然后，按`esc`按键后，输入`:wq`保存并退出文件，为了使配置生效，需要重新启动系统，然后使用sestatus命令检查selinux的状态，如下所示：

```sh
sestatus
```

## 2.3 修改`mariadb.service`

systemd 默认配置了对`/root`和`/home`等目录的限制，`ProtectHome=true`配置意味着启动时应用对这些目录不可写，mariaDB同样有这个限制。

通过以下命令可以找到`mriadb.service`的位置:

```sh
~ find / -name "mariadb.service"
```

然后使用`vi` 编辑文件，通过以下命令可以找到`ProtectHome`的位置:

```sh
: /ProtectHome*
```

找到配置位置后，将`ProtectHome=true`修改为`ProtectHome=false`，保存并退出。

执行一下命令来重启MariaDB：

```sh
~ systemctl daemon-reload
~ systemctl restart mariadb.servic
```

# 3. 总结

实际上问题的出现来源于三个方面

- 更换mariadb目录没有对目录进行授权
- selinux
- systemd 默认配置了对`/root`和`/home`等目录的限制
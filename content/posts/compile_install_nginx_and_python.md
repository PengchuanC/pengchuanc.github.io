---
title: "Centos7 编译安装Nginx-1.21.3版本呢和Python-3.10"
date: 2021-10-22T10:42:05+08:00
draft: false
toc: false
images:
tags: 
  - Nginx-1.21.3
  - Python-3.10.0
  - CentOS 7
  - RedHat 7
---



# 一、起因

由于生产网段与测试网段隔离，但测试网段也需要数据来进行开发，于是考虑用GRPC来中转数据，并用Nginx来代理端口，需要用到Nginx的ssl相关插件，刚好Python-3.10发布，也需要升级openssl-1.1.1及以上，所以不妨将Nginx和Python都升级了。



# 二、安装

## 1.安装openssl-1.1.1l

### 1.1 安装依赖

```bash
# yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel
```

### 1.2 下载并安装

下载并解压

```bash
# cd ~/Downloads
# wget https://www.openssl.org/source/openssl-1.1.1l.tar.gz --no-check-certificate
# tar -xf openssl-1.1.1l.tar.gz && cd openssl-1.1.1l
```

开始编译安装

```bash
# ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl shared zlib
# make
# make test
# make install
```

### 1.3 软链

备份

```bash
# mv /usr/bin/openssl /usr/bin/openssl.old
# mv /usr/lib64/openssl /usr/lib64/openssl.old
# mv /usr/lib64/libssl.so /usr/lib64/libssl.so.old
```

重新软链

```bash
# ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
# ln -s /usr/local/openssl/include/openssl /usr/include/openssl
# ln -s /usr/local/openssl/lib/libssl.so /usr/lib64/libssl.so
# echo "/usr/local/openssl/lib" >> /etc/ld.so.conf
# ldconfig -v 
```



## 2.安装Python 3.10

### 2.1 下载并解压

```bash
# cd ~/Downloads
# wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
# tar -xf Python-3.10.0.tgz && cd Python-3.10.0
```

### 2.2 编译安装

这里遇到了个大坑，由于Python 3.10刚出，安装资料也比较少，用了很久才把ssl模块编译进去，后来根据编译提示才知道，主要是在编译时没加`--with-openssl-rpath=auto`命令，导致ssl模块编译不进去。

```bash
# ./configure --prefix=/usr/local/python3 --with-ssl-default-suites=openssl  --with-openssl=/usr/local/openssl --with-openssl-rpath=auto
# make
# make install
```

重新链接

```bash
# mv mv /usr/bin/python3 /usr/bin/python3.old
# ln -s /usr/local/python3/bin/python3 /usr/bin/python3 
# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3 
```



## 3.安装Nginx 1.21.3

### 3.1 下载并解压

```bash
# wget http://nginx.org/download/nginx-1.21.3.tar.gz --no-check-certificate
# tar -xf nginx-1.21.3.tar.gz && cd nginx-1.21.3
```

### 3.2 编译安装

这里在编译时又遇到问题，指定的ssl位置老是报出缺失文件错误，需要把之前安装的openssl拷贝到指定位置才行。

拷贝openssl

```bash
# cp -r /usr/local/openssl /usr/local/.openssl
```

编译安装

```bash
# ./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie' --with-openssl=/usr/local
```

上述指令中部分内容可自行更改，比如log位置，启动用户，pid位置，二进制文件位置等，但要代理grpc，`--with-http_v2_module`和`--with-http_ssl_module`指令是必须的。

```bash
# make
# make install
```

查看安装结果

```bash
# nginx -V
```

结果应当如下

```
nginx version: nginx/1.21.3
built by gcc 9.3.0 (GCC) 
built with OpenSSL 1.1.1l  24 Aug 2021
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie' --with-openssl=/usr/local
```




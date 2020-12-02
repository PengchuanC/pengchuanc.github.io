---
title: "记录GRPC在各种语言下的编译方式"
date: 2020-12-02T17:42:12+08:00
draft: false
toc: false
images:
tags: 
  - RPC
---


# Python

### Python中的编译方式

假设当前工作目录为`protobuf`，待编译文件为`hello.proto`
```sh
> cd protobuf
> python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. hello.proto
```


# Go

### Golang中的编译方式

```sh
> cd protobuf
> protoc --go_out=plugins=grpc:. hello.proto
```
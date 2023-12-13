---
title: "【FOF】客户问卷管理系统"
date: 2021-11-29T16:08:21+08:00
draft: false
toc: false
images:
tags: 
  - FOF
  - Python
  - SMA
---

## 一、系统介绍

除了柜台的合格投资者认定测评问卷外，野村东方证券FOF团队还为SMA客户定制了另一套问卷，用于测定客户风险偏好和承受能力，以便为客户提供定制化的投资方案，根据问卷结果，会将客户分为S1-S5共5档风险等级，为客户提供资产配置方案，根据问卷中的投资期限和流动性偏好，为客户定制现金流。

## 二、系统展示

### 1.前端页面

前端页面为客户填写页面，客户登记后便可填写自己的SMA测评问卷。

主页面：

![front1-1](/images/question/1-1.png)

认证页：

![front1-2](/images/question/1-2.png)

文字较长的选项展示方式：

![front1-3](/images/question/1-3.png)

常规文字长度选项展示方式：

![front1-4](/images/question/1-4.png)

问卷完成后的提示：

![front1-5](/images/question/1-5.png)

### 3.后端页面

后端主要供SMA管理员使用，可以对客户问卷进行存档，查看客户需求和确定客户风险偏好。

后端首页（风险揭示）：

![front2-1](/images/question/2-1.png)

客户问卷汇总查看：

![front2-2](/images/question/2-2.png)

查看客户问卷详情：

![front2-3](/images/question/2-3.png)

## 三、技术栈

项目基于Python的Django框架，由于项目比较简单，故采用MVT模式，不再进行前后端分离开发，前端页面主要使用jQuery插件来进行交互操作。
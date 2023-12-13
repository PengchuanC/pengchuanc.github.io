---
title: "【FOF】SMA业务客户服务平台"
date: 2021-11-25T16:55:17+08:00
draft: false
toc: false
images:
tags: 
  - fof
  - sma
  - python
---

## 一、系统介绍

野村东方国际证券资管部FOF团队除了提供集合FOF产品外，还会为高净值客户提供SMA单一资管计划，关于什么是SMA，可以[点击这里](https://sma_client.nomuraoi-sec.com)查看我们的介绍页面。

对于已经购买SMA单一FOF的客户，我们会每日披露产品的运作情况，由于每日披露信息，传统的短信通知客户净值的方式不仅会打扰到客户，并且无法承载太多的信息，于是开发了**SMA客户服务平台**，目前经过一次迭代升级，初版系统将内容展示为一页纸大小，涵盖产品的业绩分析和持仓、交易流水等信息，由于业务发展需要，我们升级了初代系统，提供更多的信息以及优化的展示方式。

当前v2版系统主要功能：

1. 登入登出
2. 个人中心
3. 首页
4. 账户信息
5. 业绩表现
6. 投资记录
7. 关于我们

对于NOI SMA客户，可前往[SMA客户服务平台](https://sma.nomuraoi-sec.com/)查看

## 二、功能模块介绍

### 1.登入登出

SMA客户服务平台只是针对SMA单一FOF这一类产品，但购买了资管产品的客户可以直接在公司官网查看产品信息，为了方便客户登录，我们采用了与官网相同的登录验证逻辑，即”身份证号码“+”手机号码“+”验证码“的验证流程。

登录界面1，输入开户登记的有效证件号码：

![login1-1](/images/client-services/1-1.png)

登录界面2，输入开户登记的手机号码以获取验证码，手机号不一致则不会下发验证码：

![login1-2](/images/client-services/1-2.png)

输入正确的验证码后便可进入客户服务平台的个人中心。

### 2.个人中心

对于仅购买了一个单一资管计划的客户，将不会进入个人中心，而是直接定位到首页；对于购买多个单一资管计划的客户，在个人中心选择一个产品，即可进入该产品的首页。

预览图如下（重要信息不展示）：

![login2-1](/images/client-services/2-1.png)

### 3.首页

首页是产品基础信息的汇总，包括当前的资产净值情况，各类资产占比、市场资讯、产品公告、FOF团队专栏文章和留言功能。

预览图如下：

![home3-1](/images/client-services/3-1.png)

资讯展开：

![home3-2](/images/client-services/3-2.png)

专栏展开：

![home3-3](/images/client-services/3-3.png)

### 4.账户信息

展示资产配置情况和持有基金的持仓情况。

图表预览如下：

![account4-1](/images/client-services/4-1.png)

![account4-2](/images/client-services/4-2.png)

点击持仓基金可显示交易情况：

![account4-3](/images/client-services/4-3.png)

### 5.业绩表现

1.不同区间段产品业绩表现：

![profit5-1](/images/client-services/5-1.png)

点击费用可以查看区间产品层面产生的费用：

![profit5-2](/images/client-services/5-2.png)

2.分阶段累计收益情况

![profit5-3](/images/client-services/5-3.png)

3.净值曲线

![profit5-4](/images/client-services/5-4.png)

### 6.交易记录

交易记录预览如下：

![transaction6-1](/images/client-services/6-1.png)

## 三、技术栈

### 1.数据库

数据库采用MySQL，数据处理难点在于对接恒生的O3.2系统和FA估值系统。

### 2.后端

后端采用Python Django框架集成DRF插件做认证和权限管理，权限管理根据官网认证方式做了相应扩展，保证从官网已登录的客户到SMA服务平台可以直接查看产品信息。

后端项目可前往[PengchuanC/am_sma: am sma project (github.com)](https://github.com/PengchuanC/am_sma)查看。

### 3.前端

前端采用Vue 2.x框架。

前端项目可前往[PengchuanC/sma_front_second: sma client server second version (github.com)](https://github.com/PengchuanC/sma_front_second)查看。
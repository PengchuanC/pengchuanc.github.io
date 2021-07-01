---
title: "野村基金筛选系统第二版"
date: 2021-07-01T17:06:30+08:00
draft: false
tags:
 - FOF
 - 基金筛选
---


# 

> 在第一版的基础上优化了布局，重新设计了基金详情页的界面，并且新增了基金筛选功能和基金看板功能、ETF资金流向统计等功能

# 开发框架升级到vue3

1.	开发框架从vue2+view design更改为vue3+element plus，提供更好的性能和交互体验。

2.	使用[typescript](https://www.tslang.cn/)开发。

3.	使用vite，保证快速冷启动和即时热更新，以及真正的按需编译。

# 性能优化

性能优化除前端改进外，后端框架也进行重构：
1.	基金筛选和基金池构建部分完全重构；
2.	数据用量较大的地方使用redis缓存数据；
3.	部分接口进行异步改造，避免界面堵塞；
4.	后端数据同步程序进行多线程改造。


# 界面展示

## 首页

![home](/images/fund/home.png)

## 基金筛选

![screen](/images/fund/cart.png)

## 基金看板

![dashboard](/images/fund/dashboard1.png)

![dashboard-expanded](/images/fund/dashboard2.png)

## 热点新闻

![news](/images/fund/news.png)

## 个基信息

![outlook](/images/fund/info1.png)

![risk](/images/fund/info3.png)

![asset-allocate](/images/fund/info2.png)

## ETF资金流向

![etf-outlook](/images/fund/etf1.png)

![by-category](/images/fund/etf2.png)

![recent](/images/fund/etf3.png)



如果觉得还不错，可以去[项目首页](https://github.com/PengchuanC/fund_vue3)给我一个star！
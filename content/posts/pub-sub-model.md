---
title: "发布/订阅模式"
date: 2020-12-04T18:06:42+08:00
draft: false
toc: false
images:
tags: 
  - golang
  - 设计模式
  - 发布订阅模式
---

发布订阅模式比较常用，近期使用grpc也涉及到连接管理简单记录一下发布订阅模式的实现，主要使用chan来传输数据

也可以考虑使用回调函数来处理publish的内容


## 定义Publisher

首先定义一个Publish的struct，主要包含Subscribers属性来管理订阅者，订阅者必须使用指针来保证数据传递

```golang
// Publisher 发布者
// 管理订阅者
// 发布内容
type Publisher struct {
	sync.RWMutex
	Subscribers map[string]*Subscriber
	waitGroup sync.WaitGroup
}

func NewPublisher() *Publisher {
	return &Publisher{
		Subscribers: make(map[string]*Subscriber),
	}
}
```

接下来实现Publisher的基础功能

```golang

// 发布者的功能
// 添加订阅者
func (p *Publisher) AddSubscriber(s *Subscriber) {
	p.Lock()
	p.Subscribers[s.Name] = s
	p.Unlock()
	fmt.Printf("添加订阅者%s成功\n", s.Name)
}

// 删除订阅者
func (p *Publisher) RemoveSubscriber(name string) {
	p.Lock()
	if _, ok := p.Subscribers[name]; ok {
		delete(p.Subscribers, name)
	}
	p.Unlock()
	fmt.Printf("移除订阅者%s成功\n", name)
}

// 发布内容
func (p *Publisher) Publish(msg string) {
	p.RLock()
	defer p.RUnlock()
	p.waitGroup.Add(len(p.Subscribers))
	for _, s := range p.Subscribers {
		d_ := msg
		s_ := s
		go func() {
			s_.Run(d_)
			p.waitGroup.Done()
		}()
	}
	p.waitGroup.Wait()
}
```

## 定义Subscriber

订阅者主要是接受发布者推送的数据，当然也应该包含一个唯一的标识符，可采用uuid，本文简单采用一个name(string)

```golang
type Subscriber struct {
	sync.RWMutex
	Name string
	Data chan string
}

func NewSubscriber(name string) *Subscriber {
	return &Subscriber{Name: name, Data: make(chan string)}
}
```

订阅者应当实现的功能

```golang
// 订阅者功能
// 订阅内容
func (s *Subscriber) Subscribe(p *Publisher) {
	p.AddSubscriber(s)
}

// 取消订阅
func (s *Subscriber) UnSubscribe(p *Publisher) {
	p.RemoveSubscriber(s.Name)
}

// 处理发布的内容
func (s *Subscriber) Run(msg string) {
	s.Lock()
	go func() {
		s.Data <- msg
		s.Unlock()
	}()
}
```

完整代码

```golang
// demo/subscribe/publisher.go
package subscribe

import (
	"fmt"
	"sync"
)

// Publisher 发布者
// 管理订阅者
// 发布内容
type Publisher struct {
	sync.RWMutex
	Subscribers map[string]*Subscriber
	waitGroup sync.WaitGroup
}

func NewPublisher() *Publisher {
	return &Publisher{
		Subscribers: make(map[string]*Subscriber),
	}
}

// 发布者的功能
// 添加订阅者
func (p *Publisher) AddSubscriber(s *Subscriber) {
	p.Lock()
	p.Subscribers[s.Name] = s
	p.Unlock()
	fmt.Printf("添加订阅者%s成功\n", s.Name)
}

// 删除订阅者
func (p *Publisher) RemoveSubscriber(name string) {
	p.Lock()
	if _, ok := p.Subscribers[name]; ok {
		delete(p.Subscribers, name)
	}
	p.Unlock()
	fmt.Printf("移除订阅者%s成功\n", name)
}

// 发布者事件处理 - 产生数据
func (p *Publisher) Update(){

}

// 发布内容
func (p *Publisher) Publish(msg string) {
	p.RLock()
	defer p.RUnlock()
	p.waitGroup.Add(len(p.Subscribers))
	for _, s := range p.Subscribers {
		d_ := msg
		s_ := s
		go func() {
			s_.Run(d_)
			p.waitGroup.Done()
		}()
	}
	p.waitGroup.Wait()
}

```

```golang
// demo/subscribe/subscriber.go
package subscribe

import (
	"sync"
)

// Subscriber 订阅者
// 订阅内容，等待发布者发布内容
type Subscriber struct {
	sync.RWMutex
	Name string
	Data chan string
}

func NewSubscriber(name string) *Subscriber {
	return &Subscriber{Name: name, Data: make(chan string)}
}


// 订阅者功能
// 订阅内容
func (s *Subscriber) Subscribe(p *Publisher) {
	p.AddSubscriber(s)
}

// 取消订阅
func (s *Subscriber) UnSubscribe(p *Publisher) {
	p.RemoveSubscriber(s.Name)
}

// 处理发布的内容
func (s *Subscriber) Run(msg string) {
	s.Lock()
	go func() {
		s.Data <- string
		s.Unlock()
	}()
}
```

```golang
// demo/main.go
package main

import (
  "fmt"
  "time"
  "demo/subscribe"
  "strconv"
)

func main(){
  var (
    pub *subscribe.Publiser
    sub1 *subscribe.Subscriber
    sub2 *subscribe.Subscriber
  )

  pub = subscibe.NewPublisher()

  sub1 = subscribe.NewSubscriber("pub1")
  sub2 = subscribe.NewSubscriber("pub2")
  sub1.Subscribe(pub)
  sub2.Subscribe(pub)

  go func(){
    i := 0
    for {
      if i < 100 {
        break
      }
      pub.Publish(strconv.Itoa(i))
      i ++
    }
  }()

  go func(){
    for{
      d1, ok := <- sub1.Data
      if !ok {
        continue
      }
      fmt.Print(d1)
    }
  }()

    go func(){
    for{
      d2, ok := <- sub2.Data
      if !ok {
        continue
      }
      fmt.Print(d2)
    }
  }()

  time.Sleep(10*time.Second)
}
```
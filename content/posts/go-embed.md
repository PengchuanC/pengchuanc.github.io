---
title: "Go 1.16 新特性embed在gin中使用"
date: 2021-07-02T15:14:15+08:00
draft: false
toc: false
images:
tags: 
  - golang
  - embed
  - 模板继承
  - gin
---

> 在golang1.16加入之前，编译出来的二进制文件默认是不包括非代码文件的，那么开发一个web网站，则需要将html模板文件、配置文件和静态资源文件(css、js)始终按照开发时的目录结构放在一起，部署起来很麻烦。

embed是在Go 1.16中新加包。它通过`//go:embed`指令，可以在编译阶段将静态资源文件打包进编译好的程序中，并提供访问这些文件的能力。

### 1.使用gin框架构建一个简单的静态资源服务器

使用gin构建一个web服务非常简单，使用embed加入静态资源也非常简单，代码如下：
```go
package main

import (
	"embed"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

//go:embed statics/* templates/*
var Assets embed.FS

func main() {
	router := gin.Default()
	router.StaticFS("/", http.FS(Assets))

	err := router.Run("0.0.0.0:5000")
	if err != nil {
		fmt.Println(err)
		return
	}
}
```

文件目录结构如下：

[目录1](/images/gin-embed/tree1.png)

启动之后我们访问`http://127.0.0.1:5000`即可看到如下界面：

[初始界面](/images/gin-embed/web1.png)

### 2.在模板语言中使用静态资源

加入embed之后，gin使用模板引擎主要通过自带的方法*SetHTMLTemplate*来加载从embed中解析的模板文件，
接下来对项目结构进行以下修改以避免路由冲突，然后来渲染一个简单的页面。

此时项目目录结构如下：

[目录2](/images/gin-embed/tree2.png)

新增的`statics.go`主要是为了加载静态资源时保证路由的名称合理，其内容如下
```go
package statics

import "embed"

//go:embed css/* js/*
var Statics embed.FS
```


`main.go`文件内容修改后为：


```go
package main

import (
	"embed"
	"fmt"
	"gin_embed/statics"
	"github.com/gin-gonic/gin"
	"html/template"
	"net/http"
)

//go:embed templates/*
var Templates embed.FS

func main() {
	router := gin.Default()
	router.StaticFS("/statics", http.FS(statics.Statics))
	tmpl, _ := template.ParseFS(Templates, "templates/*")

	router.GET("/layout", index)
	router.SetHTMLTemplate(tmpl)

	err := router.Run("0.0.0.0:5000")
	if err != nil {
		fmt.Println(err)
		return
	}
}

func index(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "layouts.tmpl", gin.H{"title": "布局页面"})
}

```

`layouts.tmpl`文件内容为：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <title>{{.title}}</title>
    <link href="/statics/css/semantic.css" rel="stylesheet" type="text/css">
    <script src="/statics/js/jquery-3.6.0.min.js"></script>
    <script src="/statics/js/semantic.min.js"></script>
</head>
<body>
<div class="ui secondary pointing menu">
    <a href="first" class="item first-menu-item active">
        第一页
    </a>
    <a class="item" href="second">
        第二页
    </a>
</div>
<div class="ui container">
    <p>我是基础页面</p>
    <button class="ui button primary">按钮</button>
</div>
</body>
</html>
```

此时进入`http://127.0.0.1:/5000/layouts`我们将能看到：

[简单界面](/images/gin-embed/web2.png)

到此，加载静态资源和简单的模板渲染就可以实现了。

### 3.多模板渲染

gin本身是不支持多模板渲染的，要进行多模板渲染，可以查看[示例代码](https://github.com/gin-contrib/multitemplate)

但在引入embed过后，我们需要对官方示例做一些调整来保证正常运行。

首先在*templates/*文件目录下新建两个文件*first.tmpl*、*second.tmpl*,
内容分别如下：
```html
{{/*first.tmpl*/}}

{{template "layouts" .}}
{{define "content"}}
<p>我是第一页</p>
{{end}}
```

```html
{{/*second.tmpl*/}}

{{template "layouts" .}}
{{define "content"}}
    <p>我是第二页</p>
{{end}}
```

修改**layouts.tmpl**,加入block块来实现继承

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <title>{{.title}}</title>
    <link href="/statics/css/semantic.css" rel="stylesheet" type="text/css">
    <script src="/statics/js/jquery-3.6.0.min.js"></script>
    <script src="/statics/js/semantic.min.js"></script>
</head>
<body>
<div class="ui secondary pointing menu">
    <a href="first" class="item first-menu-item active">
        第一页
    </a>
    <a class="item" href="second">
        第二页
    </a>
</div>
<div class="ui container">
    <p>我是基础页面</p>
    <button class="ui button primary">按钮</button>
    {{block "content" .}}{{end}}
</div>
</body>
</html>
```

**main.go**修改如下

```go
package main

import (
	"embed"
	"fmt"
	"gin_embed/statics"
	"github.com/gin-contrib/multitemplate"
	"github.com/gin-gonic/gin"
	"html/template"
	"net/http"
)

//go:embed templates/*
var Templates embed.FS

func main() {
	router := gin.Default()
	router.StaticFS("/statics", http.FS(statics.Statics))

	router.GET("/first", first)
	router.GET("/second", second)
	router.HTMLRender = CreateMyRender()

	err := router.Run("0.0.0.0:5000")
	if err != nil {
		fmt.Println(err)
		return
	}
}


type Render struct {
	render multitemplate.Render
	assets embed.FS
}


func (r *Render) AddFromEmbed (name string, patterns ...string) {
	tmpl, err := template.ParseFS(r.assets, patterns...)
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	r.render.Add(name, tmpl)
}

func CreateMyRender() multitemplate.Renderer {
	var render Render
	render = Render{
		render: multitemplate.New(),
		assets: Templates,
	}

	render.AddFromEmbed("layouts", "templates/layouts.tmpl")
	render.AddFromEmbed("first", "templates/layouts.tmpl", "templates/first.tmpl")
	render.AddFromEmbed("second", "templates/layouts.tmpl", "templates/second.tmpl")

	return render.render
}


func first(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "first", gin.H{"title": "第一页"})
}

func second(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "second", gin.H{"title": "第二页"})
}

```

再次启动后进入`http://127.0.0.1/first`后界面如下：

[界面3](/images/gin-embed/web3.png)

最终项目结构如下：

[目录3](/images/gin-embed/tree3.png)

完整代码可前往我的[GitHub](https://github.com/PengchuanC/pengchuanc.github.io/tree/main/src)项目查看.
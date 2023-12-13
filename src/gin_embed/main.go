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

package statics

import "embed"

//go:embed css/* js/*
var Statics embed.FS

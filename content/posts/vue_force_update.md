---
title: "Vue3解决数组改变界面没有重新刷新的问题"
date: 2021-05-19T10:07:04+08:00
draft: false
tags:
 - Vue3
 - 数组刷新
---

### 解决方法

在使用vue3或vue2时，时常遇到数组或对象更新，但在列表渲染的UI却没有随数据改变而刷新，这是由于 JavaScript 的限制，Vue 不能检测数组的变动，如果要更新数组，可以采用`push`、`splice`、`concat`等方法，对象可以使用`assign`方法，如果以上方法不生效，可以强制刷新页面，主要是通过修改列表渲染的`key`来实现，vue在修改`key`时，会强制刷新页面。

#### 1.简单解决

```vue
<template>
	<div :key="state.updateKey">
        <div>
            ...
    	</div>
    </div>
</template>

<javascript>
    import ...
    
	export default({
    	setup(){
    		const state = reactive({
    			updateKey: 0
    		})
    	}
    
    	const updateArray = ()=>{
    		...
    		state.updateKey ++
    	}
    	return { state }
    })
</javascript>
```

#### 2.复杂方式

在列表渲染时保证每一个tag的`key`是唯一的，也就是不要直接使用`index`作为`key`，这样array变化后，`key`也会变动，页面自然就刷新了。
---
title: "利用Nginx和Daphne部署Django3.x和Django channels 3.x"
date: 2020-12-02T18:13:44+08:00
draft: false
toc: false
images:
tags: 
  - Django
  - Python
  - Asgi
---

Django在3.0正式引入asgi，部署方式与2.x略有不同


## 仅部署http网站

如果仅部署http网站，可采用uvicorn来进行部署，然后通过nginx代理地址即可

```sh
> cd [your_project]
> nohup uvicorn [your_project].asgi:application --host 0.0.0.0 --port 5000 > asgi.log &
```

```conf
server {
  location / {
    proxy_pass http://0.0.0.0:5000;
  }
}
```

## 部署http和websocket

Django中websocket功能主要通过[django-channels](https://channels.readthedocs.io/en/stable/)组件实现，由于引入了ws，部署方式略有不同

官方推荐使用daphne部署

以我当前的`sma_management`项目为例，django3.x版本中，在 `sma_management/sma_management/`目录下应当有`asgi.py`文件，引入channels后，应当如下：
```python
import os
import django
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sma_management.settings")
django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import investment.routing


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            investment.routing.websocket_urlpatterns
        )
    ),
})
```
其中`django.setup()`命令必须在channels相关业务前引入，不然daphne启动服务会抛出错误

配置好`asgi.py`后，仅需在项目目录中启动shell，输入：
```sh
> nohup daphne -p 8000 sma_management.asgi:application > daphne.log &
```
http和ws服务均使用8000端口，使用Nginx代理的话，配置如下：
```conf

upstream channels-backend {
    server localhost:8000;
}

server {
  location /management {
      proxy_pass http://0.0.0.0:8000;
  }

  location /ws {
      proxy_pass http://channels-backend;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";

      proxy_redirect off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $server_name;
  }
}

```

这样便可以使用 http://0.0.0.0/management/访问http服务，使用ws://0.0.0.0/ws/访问ws服务
---
title: "Python中使用JWT"
date: 2020-12-21T11:18:59+08:00
draft: false
toc: false
images:
tags: 
  - python
  - jwt
  - authorization
---

在前后端分离的web项目中，后端一般采用Restful Api，这种模式的后端是无状态的，

不便再使用Session这种传统的认证方式，一般采用**JWT**。

基于jwt的鉴权机制也是无状态的，因此不需要在服务端去保留用户的认证信息或者会话信息，jwt是存储在客户端的，服务器端不需要存储jwt的，客户端每次发送请求时会携带该token，然后到服务器端会验证token是否正确，是否过期了，来验证token的有效性。

再Django中，使用restframework便可以很方便的使用jwt进行认证了，我们也可以通过标准库`jwt`来简单实现jwt加解密过程。

## 1.JWT加密

jwt加密一般采用`HS256`的加密方式，为了保证jwt的安全，需要设置一个仅提供者可知的`secret key`，然后再对用户信息进行打包，代码如下：

```python
import jwt
import datetime

from itsdangerous import JSONWebSignatureSerializer


SECRET_KEY = 'iencj58^&/.+_@#%$jnckn'

# token超时时间
expire_at = (datetime.datetime.now() + datetime.timedelta(minutes=15)).timestamp()
payload = {'username': 'Asin', 'expireAt': expire_at}

token = jwt.encode(payload, key=SECRET_KEY, algorithm='HS256')
print(token)
#b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFzaW4iLCJleHBpcmVBdCI6MTYwODUyMjI1Mi44MTU5NzV9.psXYOLOgzo1mzAHzDCk2hcocMaq_D84yOoXPMhk3W8U'
```

## 2.JWT解密

解密的关键就在于`secret key`和加密方式，知道这两条信息后，解密过程就很简单了，代码如下：

```python
import jwt

token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFzaW4iLCJleHBpcmVBdCI6MTYwODUyMjI1Mi44MTU5NzV9.psXYOLOgzo1mzAHzDCk2hcocMaq_D84yOoXPMhk3W8U'

SECRET_KEY = 'iencj58^&/.+_@#%$jnckn'

info = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')
print(info)
# {'username': 'Asin', 'expireAt': 1608522252.815975}
```

### 3.使用`itsdangerous`包

`itesdangerous`是flask中推荐使用的签名工具，使用方式也相当简单。

```python
from itsdangerous import TimedJSONWebSignatureSerializer


SECRET_KEY = 'iencj58^&/.+_@#%$jnckn'


serializer = TimedJSONWebSignatureSerializer(secret_key=SECRET_KEY, algorithm_name='HS256')
# 设置超时时间为15分组
serializer.DEFAULT_EXPIRES_IN = 60 * 15
token = serializer.dumps({'username': 'Asin'})
print(token)

info = serializer.loads(token)
print(info)
```

## 4.在项目中使用

在项目中使用jwt时，一般还需要包含令牌的签发者及签发日期等信息，用于加强安全性和token超时后的刷新机制，因此认证后返回的除了token外还应该包含一条用于刷新的token，避免token频繁超时。


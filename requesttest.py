# encoding=utf-8
import requests
from requests.cookies import RequestsCookieJar
from requests.auth import HTTPBasicAuth
from requests import Request, Session
import re

def other_method():
    r = requests.get('http://www.baidu.com')
    print(type(r))
    print(r.status_code)
    print(type(r.text), r.text)
    print(r.content.decode('utf-8'))
    # <class 'requests.cookies.RequestsCookieJar'>
    print(type(r.cookies), r.cookies)
    for key, value in r.cookies.items():
        print('cookies ', key + '=' + value)
    # <class 'requests.structures.CaseInsensitiveDict'>
    print(type(r.headers), r.headers)
    # <class 'str'>
    print(type(r.url), r.url)
    # <class 'list'>
    print(type(r.history), r.history)

    print('#################  data  ###########################')
    data = {
        'name': 'jenny',
        'age': 18
    }

    headers = {
        "origin": "122.192.201.82, 122.192.201.82",
        "url": "https://httpbin.org/get"
    }
    resp = requests.get(url='http://httpbin.org/get', data=data, headers=headers)
    print(resp.content.decode())
    # 转为 json
    dict1 = resp.json()
    ''':type:dict'''
    print(type(dict1))
    for key in dict1.keys():
        print(key, dict1[key])

    print('####################### 抓取二进制文件 ############################')
    respPic = requests.get('https://github.com/favicon.ico')
    with open('githubPic.ico', 'wb') as f:
        f.write(respPic.content)

    print('####################### request 内置返回码 ############################')
    resp2 = requests.get('http://www.jianshu.com')
    exit() if not r.status_code == requests.codes.ok else print('Request Success ')

    print('####################### 文件上传 ############################')
    files = {'file': open("githubPic.ico", 'rb')}
    resUpload = requests.post('http://httpbin.org/post',files = files)
    print(resUpload.text)

def zhihu():
    print('####################### 知乎 #########################')
    # 设置 cookie 模拟登陆状态
    headers = {
        'cookie': '_zap=03ac5a4e-32e0-4cb4-94c6-74a9d59f8a16; __DAYU_PP=QZEvzRznjnaAebQznQy36426c53c8b7b; d_c0="AGDjM5uknQ2PTkqf7vDLxsJKxzIwRbO8-tY=|1526697541"; q_c1=54cdffd9f1ed442fbb97b333d4c8a785|1526697576000|1513342907000; _xsrf=ZvOEk6tHthFakbyspKkI7Z1pdV4L65xO; tgw_l7_route=116a747939468d99065d12a386ab1c5f; capsion_ticket="2|1:0|10:1559222605|14:capsion_ticket|44:OTAzZjdlNzU3OGRhNDMxMGI5ZjBlMDNkZTdhMzMyOTI=|1bd21a89059edeb5f55cd6851de7afd60a6630a16226d1f7a1d9492d14f5f9bc"; z_c0="2|1:0|10:1559222649|4:z_c0|92:Mi4xb1VnNUJnQUFBQUFBWU9Nem02U2REU1lBQUFCZ0FsVk5lU2ZkWFFEdXNCWktpWHJ2N3k1MzRfQ1lQTTVlTFliZUt3|ccbcd4de8dd0e25689898e472579ed8f5e4c32d3f1fe3cb092b0910bb855bf12"; unlock_ticket="AEACRhVsiQwmAAAAYAJVTYHg71yxTl5IEEuhipecshZMsmW5v9KIUw=="; tst=r',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'
    }
    # zhihu_rl = 'https://www.zhihu.com/'
    zhihu_rl = 'https://www.zhihu.com/question/265583638/answer/667700021'
    zhihu_resp = requests.get(zhihu_rl, headers = headers)
    print(zhihu_resp.content.decode('utf-8'))

def zhihu2():
    print('####################### 知乎 #########################')
    # 设置 cookie 模拟登陆状态
    cookies = '_zap=03ac5a4e-32e0-4cb4-94c6-74a9d59f8a16; __DAYU_PP=QZEvzRznjnaAebQznQy36426c53c8b7b; d_c0="AGDjM5uknQ2PTkqf7vDLxsJKxzIwRbO8-tY=|1526697541"; q_c1=54cdffd9f1ed442fbb97b333d4c8a785|1526697576000|1513342907000; _xsrf=ZvOEk6tHthFakbyspKkI7Z1pdV4L65xO; tgw_l7_route=116a747939468d99065d12a386ab1c5f; capsion_ticket="2|1:0|10:1559222605|14:capsion_ticket|44:OTAzZjdlNzU3OGRhNDMxMGI5ZjBlMDNkZTdhMzMyOTI=|1bd21a89059edeb5f55cd6851de7afd60a6630a16226d1f7a1d9492d14f5f9bc"; z_c0="2|1:0|10:1559222649|4:z_c0|92:Mi4xb1VnNUJnQUFBQUFBWU9Nem02U2REU1lBQUFCZ0FsVk5lU2ZkWFFEdXNCWktpWHJ2N3k1MzRfQ1lQTTVlTFliZUt3|ccbcd4de8dd0e25689898e472579ed8f5e4c32d3f1fe3cb092b0910bb855bf12"; unlock_ticket="AEACRhVsiQwmAAAAYAJVTYHg71yxTl5IEEuhipecshZMsmW5v9KIUw=="; tst=r'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'
    }

    jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar.set(key, value)

    zhihu_rl = 'https://www.zhihu.com/question/265583638/answer/667700021'
    zhihu_resp = requests.get(zhihu_rl, headers = headers, cookies = jar)
    print(zhihu_resp.content.decode('utf-8'))

def session_test():
    print('################### session() ###########################')
    s = requests.Session()
    s.get('http://httpbin.org/cookies/set/number/123456789')
    res = s.get('http://httpbin.org/cookies')
    print(res.text)

def proxy_test():
    # 测试代理
    proxies = {
        'http': 'http://user:password@10.10.1.10:3128/'  # HTTP Basic Auth 代理
    }

    requests.get('https://www.taobao.com', proxies = proxies)

    # SOCKS 协议代理 需要安装 socks 这个库     pip3 install requests[socks]

    proxies2 = {
        'http': 'socks://user:password@host:port',
        'https': 'socks://user:password@host:port'
    }
    requests.get('https://www.taobao.com', proxies = proxies2)

def timeout_test():
    # 1 为 连接和读取这两者timeout的总和
    # resp = requests.get('https://www.taobao.com', timeout=1)

    # 分别设置连接和读取的timeout
    # resp = requests.get('https://www.taobao.com', timeout=(2,10))

    # None或者不设置 表示永不超时
    resp = requests.get('https://www.taobao.com', timeout=None)
    print(resp.status_code)

def auth_test():
    print('############## 身份认证 ###################')
    r = requests.get('', auth=HTTPBasicAuth('username', 'passowrd'))
    # 使用元组 代替 HTTPBasicAuth
    r = requests.get('', auth=('username', 'passowrd'))
    print(r.status_code)

def prepared_requset():
    url = 'http://httpbin.org/post'
    data = {
        'name': 'zhangsan'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'
    }
    s = Session()
    # 将各个参数通过一个 Request 对象表示
    req = Request(method='POST', url=url, data=data, headers=headers)
    # 将 Request 对象放入session中
    prepared = s.prepare_request(req)
    # 发送请求
    resp = s.send(prepared)
    print(resp.text)

if __name__ == '__main__':
    # zhihu2()
    # session_test()
    # proxy_test()
    # timeout_test()
    prepared_requset()
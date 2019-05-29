from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, ProxyHandler
from urllib import error
import http.cookiejar, urllib.request

from http.client import HTTPResponse
from http.cookiejar import Cookie

'''
HITPDefaultErrorHandler ：用于处理 HTTP 响应错误，错误都会抛出 HTTP Error 类型的异常 。
HTTPRedirectHandler ：用于处理重定向 。
HTTPCookieProcessor ： 用于处理 Cookies 。
ProxyHandler ：用于设置代理 ， 默认代理为空 。
HπPPasswordMgr ：用于管理密码，它维护了用户名和密码的表 。
HTTPBasicAuthHandler ： 用于管理认证，如果一个链接打开时需要认证，那么可以用它来解决认证问题。
'''

print('######################## 验证用户名密码 #############################')

username = 'username'
password = 'password'
url = 'https://www.baidu.com'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url, timeout=0.1)
    ''':type:HTTPResponse'''
    html = result.read().decode('utf-8')
    print(html)
except error.URLError as ex:
    print(ex.reason)

print('######################## 代理 #############################')

# 本地搭建了一个代理，运行在9743端口上
proxy_handler = ProxyHandler({
    'http': 'http://127.0.0.1:9743',
    'https': 'https://127.0.0.1:9743'
})
opener2 = build_opener(proxy_handler)
try:
    response = opener2.open("https://www.baidu.com")
    ''':type:HTTPResponse'''
    print(response.read().decode('utf-8'))
except error.URLError as e:
    print(e.reason)

print('######################## Cookies #############################')

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookiejar=cookie)
opener = urllib.request.build_opener(handler)
response = opener.open("http://www.baidu.com")
for item in cookie: # type: Cookie
    print(item.name + '\t' + item.value)

# 保存 cookie 保存成 Mozilla 型浏览器的 Cookies 格式 。
filename = 'cookie1.txt'
cookie2 = http.cookiejar.MozillaCookieJar(filename)
handler2 = urllib.request.HTTPCookieProcessor(cookie2)
opener2 = urllib.request.build_opener(handler2)
response2 = opener2.open("http://www.baidu.com")
cookie2.save(ignore_discard=True, ignore_expires= True)

# 保存成 libwww-perl(LWP）格式的 Cookies 文件
filename2 = 'cookie2.txt'
cookie3 = http.cookiejar.LWPCookieJar(filename2)
handler3 = urllib.request.HTTPCookieProcessor(cookie3)
opener3 = urllib.request.build_opener(handler3)
response3 = opener3.open("http://www.baidu.com")
cookie3.save(ignore_discard=True, ignore_expires= True)

# 读取cookie
print('######################## 读取 Cookie #############################')
cookie4 = http.cookiejar.LWPCookieJar()
cookie4.load(filename2, ignore_discard=True, ignore_expires=True)
handler4 = urllib.request.HTTPCookieProcessor(cookie4)
opener4 = urllib.request.build_opener(handler4)
response4 = opener4.open('http://www.baidu.com')
print(response.read().decode('utf-8'))

# encoding=utf-8
import requests
import re

r = requests.get('http://www.baidu.com')
print(type(r))
print(r.status_code)
print(type(r.text), r.text)
print(r.content.decode('utf-8'))
# <class 'requests.cookies.RequestsCookieJar'>
print(type(r.cookies), r.cookies)
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


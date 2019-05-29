# encode=utf-8
from urllib import request, parse
import urllib.error
import socket
from http.client import HTTPResponse
from urllib.parse import urlparse, ParseResult, urlunparse, urlencode
from urllib.parse import parse_qs, parse_qsl, quote, unquote
from urllib.robotparser import RobotFileParser
import lxml

# url = 'https://talent.baidu.com/baidu/web/httpservice/userCheckLogin'
url = ' https://www.python.org'
# url = 'https://www.baidu.com'
url_agent = ''
# 类型注解 IDE 会有提示
response = urllib.request.urlopen(url) # type: HTTPResponse
# 打印 response 类型
print(type(response))
print(response.getheaders())
print(response.getheader('Server'))
# print(response.read().decode('utf-8'))

print('########################## 带参数的请求 ################################')
data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf-8')
responseData = request.urlopen('http://httpbin.org/post', data=data)
# 指定 responseData 类型为 HTTPResponse IDE 有提示
''':type:HTTPResponse'''
print(responseData.read().decode('utf-8'))

print('######################## 设置时间超时处理 #############################')
try:
    responseTime = urllib.request.urlopen("http://httpbin.org/get", timeout=0.1) # type: HTTPResponse
except urllib.error.URLError as ex:
    if isinstance(ex.reason, socket.timeout):
        ''' 判断ex.reason 是否为 socket.timeout 类型 '''
        print(" time out error ! ")

print('######################## request #############################')

url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE S. S; Windows NT)',
    'Host': 'httpbin.org'
}
paramDict = {
    'name': 'Germey'
}
data = bytes(urllib.parse.urlencode(paramDict), 'utf-8')
req = request.Request(url=url, data = data, headers=headers, method='POST')
# req.add_header('','')
response2 = request.urlopen(req)
''':type:HTTPResponse'''
print(response2.read().decode('utf-8'))


print('######################## urlparse #############################')
result = urlparse('https://www.hao123.com/feedData/data?type=rec&callback=jQuery')
''':type:ParseResult'''
print(type(result))
print(result)
print(result.scheme, result[0], result.netloc, result[1], sep='\n')


print('######################## urlunparse #############################')
# 必须是 6 个元素
data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))

# urlsplit()    urlunsplit()    urljoin()
# urlencode() 序列化参数
base_url = 'http://www.baidu.com'
params = {
    'name': '张三',
    'age': 16
}
url = base_url + urlencode(params)
print(url)

#
query = 'name=danny&age=21'
# parse_qs 将参数转为 字典
print(parse_qs(query))
# parse_qsl 将参数转为元组组成的列表
print(parse_qsl(query))

# quote url编码
keyword = params.get('name')
url = 'http://www.baidu.com?wd=' + quote(keyword)
print(url)

# unquote url解码
print(unquote(url))

# 判断一个爬取爬虫是否有权限爬取这个网站
print('######################## robotparser #############################')
rp = RobotFileParser()
# robots.txt 地址
rp.set_url('https://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', '/search'))
print(rp.can_fetch('*', 'https://www.jianshu.com/p/75d5ea56ec7f'))





# encode=utf-8
import urllib.request
import lxml

url = 'https://talent.baidu.com/baidu/web/httpservice/userCheckLogin'
# url = 'https://www.baidu.com'
url_agent = ''
response = urllib.request.urlopen(url)
html = response.read();
print('html = %s' % html)




# encoding=utf-8
import re
import requests
import json
import time
# 获取页面
def get_one_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101'
                      ' Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200 :
        return response.text
    return None

# 解析html
def parse_one_page(html):
    pattern = re.compile('<dd>.*?<i class="board-index.*?>(.*?)</i>.*?<img data-src="(.*?)".*?<p class="name">'
                         '<a href=".*?">(.*?)</a></p>.*?<p class="star">(.*?)</p>.<p class="releasetime">(.*?)'
                         '</p>.*?<i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    results = re.findall(pattern, html)
    for item in results:
        # print(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
        yield {
            'rank': item[0],
            'image': item[1],
            'name': item[2],
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

# 写入文件
def write_to_file(content):
    with open('movie.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        # dumps实现字典的序列化  ensure_ascii=False 保证输出的是中文不是Unicode编码
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

# 分页查询
def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        # 增加一个延时等待，避免反爬虫
        time.sleep(1)

if __name__ == '__main__':
    for i in range(10):
        main(offset= i * 10)
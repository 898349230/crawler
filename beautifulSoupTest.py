# encoding=utf-8
from bs4 import BeautifulSoup
import re

def test01():
    soup = BeautifulSoup('<p>Hello</p>', 'lxml')
    print(soup.p.string)

html = '''
<html> <head ><title>The Dormouse's story</title></head>
<body >
<p class="title" name="dromouse"><b>The Dormouse ’s story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href=" http://example.com/elsie" class="sister" id="link1"><!-- Elsie -- ></a>,
<a href=" http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a> ;
and they lived at the bottom of a well . </p>
<p class="story"> ... </p>
'''

def test02():
    # 要解析的字符串 和 解析器类型， 初始化的时候会将不标准的 html 进行自动更正格式
    soup = BeautifulSoup(html, 'lxml')
    # 将html以标准的缩进格式输出
    print(soup.prettify())
    print('****************************************************')
    print(soup.title)
    print(type('title'))
    # 获取 title 格式内容。 string 获取内容
    print(soup.title.string)
    print(soup.head)
    # 默认会获取第一个 p 节点的内容
    print(soup.p)
    # 获取属性
    print('************************  属性  ******************************')
    print(soup.p.attrs)  # 返回是字典
    print(soup.p.attrs['name'], '  ', soup.p['class'])

    print('***************** 嵌套获取 ********************')
    print(soup.head.title.string)

def child_test():
    html = '''
        <html>
        <head>
        <title>The Dormouse's story</title>
        </head>
        <body>
        <p class="story">
            Once upon a time there were three little sisters;and their names were
            <a href="http://example.com/elsie" class="sister" id= "link1">
            <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id=" link2">Lacie</a>
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class=" story"> .. . </p>
        '''
    soup = BeautifulSoup(html, 'lxml')
    # 返回列表形式, contents 返回直接子节点的列表
    print(soup.p.contents)
    # children 返回直接子节点列表
    print('children  ', soup.p.children)
    for i, child in enumerate(soup.p.children):
        print(i, child)

    # descendants 返回所有子孙节点
    print('all children', '  ', soup.p.descendants)
    for i, child in enumerate(soup.p.descendants):
        print(i, '  ', child)

    print('parents  ', list(enumerate(soup.a.parents)))
    # 获取父节点
    print('text  ', list(soup.a.parents)[0])
    # attrs 获取 class 属性
    print('attrs  ', list(soup.a.parents)[0].attrs['class'])
    print('next sibling  ', soup.a.next_siblings)
    print('next sibling  ', list(enumerate(soup.a.next_siblings)))
    print('previous sibling  ', list(enumerate(soup.a.previous_siblings)))

def find_all_test():
    soup = BeautifulSoup(html, 'lxml')
    print(soup.find_all(name='p'))
    # bs4.element.Tag 类型
    print(type(soup.find_all(name='p')[0]))
    # 根据属性查找
    print('attr ', soup.find_all(attrs={'class', 'story'}))
    # 文本匹配
    print('text ', soup.find_all(text=re.compile('names')))
    # find() 查询第一个符合条件的节点
    # find_parents() find_parent()
    # find_next_siblings() find_next_sibling()
    # find_previous_siblings() find_previous_sibling()
    # find_all_next() find_next()
    # find_all_previous() find_previous()

def css_test():
    print('********************  css选择器   ********************************')
    html = '''
            <html>
            <head>
            <title>The Dormouse's story</title>
            </head>
            <body>
            <p class="story">
                Once upon a time there were three little sisters;and their names were
                <a href="http://example.com/elsie" class="sister1" id= "link1">
                <span>Elsie</span>
                </a>
                <a href="http://example.com/lacie" class="sister2" id=" link2">Lacie</a>
                and
                <a href="http://example.com/tillie" class="sister3" id="link3">Tillie</a>
                and they lived at the bottom of a well.
            </p>
            <p class=" story"> .. . </p>
            '''
    soup = BeautifulSoup(html, 'lxml')
    print(soup.select('a'))
    for a in soup.select('a'):
        # 获取属性
        print('属性 ', a.attrs['class'])
        print('属性 ', a['class'])
        # 获取文本
        print('文本 ', a.get_text())
        print('文本 ', a.string)


if __name__ == '__main__':
    # test01()
    # test02()
    # child_test()
    # find_all_test()
    css_test()
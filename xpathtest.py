# encoding=utf-8
from lxml import etree
from lxml.etree import _ElementTree
from lxml.etree import Element
def html_test():
    text = '''
    <div>
    <ul>
    <li class="item-0"><a href="link1.html">first item</a></li>
    <li class="item-1"><a href="link2.html">second item</a><li>
    <li class="item-inactive"><a href="link3.html">third item</a></li>
    <li class="item-1"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="links.html">fifth item</a></li>
    </ul>
    </div>
    '''
    # 构造一个 HTML 对象， 并且自动修正 HTML 文本
    html = etree.HTML(text)
    # 输出 修正后的 HTML 代码， 但是结果是 bytes 类型
    result = etree.tostring(html)
    # decode 方法转为 str 类型
    print(result.decode('utf-8'))

def html_test2():
    html = etree.parse('./test.html', etree.HTMLParser())
    result = etree.tostring(html)
    print(result.decode('utf-8'))

'''
nodename : 选取此节点的所有子节点
/        : 从当前节点选取直接子节点
//       : 从当前节点选取子孙节点
.        : 获取当前节点
..       : 选取当前节点的父节点
@        : 选取属性
'''

# 子，子孙节点
def child_node_test():
    html = etree.parse('./test.html', etree.HTMLParser())
    print(type(html))
    #   * 匹配所有节点
    result = html.xpath('//*')
    print(result)
    # 获取 所有 li 节点， 结果为列表
    result2 = html.xpath('//li')
    print(result2, result2[0])
    # 获取 li 下的直接 a 节点
    result3 = html.xpath('//li/a')
    print(result3)
    # 获取 ul 下的 所有子孙 a 节点
    result4 = html.xpath('//ul//a')
    print(result4)

'''
<div>
    <ul>
        <li class="item-0">
            <a href="link1.html">first item</a>
        </li>
        <li class="item-1">
            <a href="link2.html">second item</a>
        <li>
        <li class="item-inactive">
            <a href="link3.html">third item</a>
        </li>
        <li class="item-1">
            <a href="link4.html">fourth item</a>
        </li>
        <li class="item-0">
            <a href="links.html">fifth item</a>
        </li>
    </ul>
</div>
'''

# 获取父节点
def father_node_test():
    html = etree.parse('./test.html', etree.HTMLParser()) # type: _ElementTree
    print(type(html))
    # 选取 href 属性为 link4.html 的 a 节点，然后获取其父节点，在获取其属性为 class 的属性
    result = html.xpath('//a[@href="link4.html"]/../@class')
    # 通过 parent:: 获取父节点
    result2 = html.xpath('//a[@href="link4.html"]/parent::*/@class')
    print(result)
    print(result2)

def attr_node_test():
    html = etree.parse('./test.html', etree.HTMLParser()) # type: _ElementTree
    # 根据属性获取节点
    result = html.xpath('//li[@class="item-0"]')
    print(result)

def text_node_test():
    html = etree.parse('./test.html', etree.HTMLParser()) # type: _ElementTree
    # 获取文本
    result = html.xpath('//li[@class="item-0"]/a/text()')
    print(result)
    # 选取 li[@class="item-0"] 下 所有的文本，会获取到 li 下 自动修正的  换行符 \n
    result2 = html.xpath('//li[@class="item-0"]//text()')
    print(result2)


def contain_node_test():
    print('****************** 一个class 中有两个 li 使用 contains **********************')
    text = '<li class="li li-first"><a href="link.html">first item</a><li>'
    html = etree.HTML(text)
    result = html.xpath('//li[contains(@class, "li")]/a/text()')
    print(result)


'''
XPath 运算符:
    or
    and
    mod ：计算余数
    | ：计算节点集
    +   -   *   div !=  < > <= >= 
'''
def attr_many_test():
    print('************************ 多属性匹配 ********************')
    text = '<li class="li li-first" name="item"><a href="link.html">first item</a><li>'
    html = etree.HTML(text)
    result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
    print(result)

def order_test():
    print('******************** 按序选择 **********************************')
    html = etree.parse('./test.html', etree.HTMLParser()) # type: _ElementTree
    result = html.xpath('//li[1]/a/text()')
    result1 = html.xpath('//li[last()]/a/text()')
    result2 = html.xpath('//li[position()<2]/a/text()')
    result3 = html.xpath('//li[last()-2]/a/text()')
    print(result)
    print(result1)
    print(result2)
    print(result3)

def zhou_test():
    print('******************** 节点轴选择 ***************************')
    html = etree.parse('./test.html', etree.HTMLParser()) # type: _ElementTree
    # 第一个 li 节点的所有祖先节点
    result1 = html.xpath('//li[1]/ancestor::*')
    print(result1)
    # 第一个 li 节点所有祖先节点的div节点
    result2 = html.xpath('//li[1]/ancestor::div')
    print(result2)
    # 第一个 li 节点的所有 attribute
    result3 = html.xpath('//li[1]/attribute::*')
    print(result3)
    # 第一个 li 节点的 子节点的 属性 href="link1.html" 的 a 节点
    result4 = html.xpath('//li[1]/child::a[@href="link1.html"]')
    print(result4)
    # 第一个 li 节点的所有 span 子孙节点
    result5 = html.xpath('//li[1]/descendant::span')
    print(result5)
    # 第一个 li 节点之后的 第二个后续节点 因为使用了 [2] 索引
    result6 = html.xpath('//li[1]/following::*[2]') # type:list
    print(result6)
    for var in result6:
        print('list  ', var.text)
    # 第一个 li 所有后续同级节点
    result7 = html.xpath('//li[1]/following-sibling::*')
    print(result7)
    for var in result7:
        print('list -> result7.text = ', var.text)
if __name__ == '__main__':
    # html_test()
    # html_test2()
    # child_node_test()
    # father_node_test()
    # attr_node_test()
    # text_node_test()
    # contain_node_test()
    # attr_many_test()
    # order_test()
    zhou_test()
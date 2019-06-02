# encoding=utf-8
import re

def match_test():
    content = 'Hello 123 4567 World_this is a Regex Demo'
    print('length: ', len(content))
    # ^表示开始
    # \s 匹配空白符
    # \d 匹配一个数字
    # \d{4} 匹配4个数字
    # \w{10} 匹配10个字符
    result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}', content)
    print('result: ', result)
    # group 匹配到的内容
    # span 输出匹配的范围 (0, 25)
    print('group: ', result.group())
    print('span: ', result.span())

def match_test2():
    content = 'Hello 1234567 World_this is a Regex Demo'
    result = re.match('^Hello\s(\d+)\sWorld', content)
    print('result: ', result)
    print('group: ', result.group())
    # group(1) 会输出第一个被 () 包裹起来的内容 group(2)则会输出第二个被 () 包裹起来的内容
    print('group1: ', result.group(1))
    print('span: ', result.span())

def match_test3():
    content = 'Hello 1234567 World_this is a Regex Demo'
    # .* 贪婪匹配，会匹配尽可能多的字符
    result = re.match('^He.*(\d+).*Demo$', content)
    # .*? 费贪婪匹配
    result2 = re.match('^He.*?(\d+).*Demo$', content)

    print('result: ', result)
    print('group1: ', result.group(1))
    print('span: ', result.span())

    print('result2: ', result2)
    print('group12: ', result2.group(1))
    print('span2: ', result2.span())

def match_test4():
    content = 'http://wwww.aaa.com/comment/abc'
    result1 = re.match('http.*?comment/(.*)', content)
    # 使用非贪婪匹配
    result2 = re.match('http.*?comment/(.*?)', content)
    print('result1 ', result1.group(1))
    # 非贪婪匹配 .*? 在字符串结尾没有匹配到字符，因为他会匹配尽可能少的字符
    print('result2 ',result2.group(1))

def match_test5():
    # 字符串中存在换行符
    content = '''Hello 1234567 World_this 
    is a Regex Demo'''
    # . 不匹配换行符
    # re.S  使.匹配包括换行符在内的所有字符
    # re.I  使匹配对大小写不敏感
    result = re.match('^He.*?(\d+).*?Demo$', content, re.S)
    print('group1: ', result.group(1))

def search_test():
    content = 'Extra strings Hello 1234567 World_this is a Regex Demo'
    # 使用 match 匹配不到， 因为match 是从字符串的开头匹配的，一旦开头不匹配，那么整个匹配就失败了
    result = re.match('He.*?(\d+).*?Demo$', content)
    # 没有匹配到会报错
    # print('match: ', result.group(1))

    # search() 会返回第一个匹配成功的结果
    result2 = re.search('He.*?(\d+).*?Demo$', content)
    print('search : ', result2.group(1))

def findall_test():
    content = '''
        </div>
            <h2 class ＝"active">经典老歌<h2>
            <li data-view="6">
                <a href="/2.mp3" singer="齐秦">往事随风</a>
            </li>
            <li data-view="7">
                <a href="/6.mp3" singer="任贤齐">沧海一卢笑</a>
            </li>        
            <li data-view="8">
                <a href="/4.mp3" singer="齐秦">往事随风</a>
            </li>
        </div>
    '''

    content2 = '''
    <div class="user-common-sites" id="userCommonSites"><div class="js_manage site-manage" title="添加网址"></div><ul class="js_bd cls_bd"><li class="js_site-item site-item" data-id="1" data-title="百度" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/5a6639075515a8e27e0b1336db2300c1.ico" data-status="1" title="百度"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="https://www.hao123.com/link/https/?key=http%3A%2F%2Fwww.baidu.com%2F%3Ftn%3Dsitehao123_15&amp;&amp;monkey=m-site&amp;c=CD192D61EB4EB67A624A8EFFE7BC4D28" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/5a6639075515a8e27e0b1336db2300c1.ico)" data-title="百度">百度</a>•<a class="sitelink sub-site" href="http://tieba.baidu.com/" data-title="贴吧">贴吧</a></div></li><li class="js_site-item site-item" data-id="2" data-title="新浪" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/10597f220b047cee3e8ea50e91886d71.ico" data-status="1" title="新浪"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="http://www.sina.com.cn/" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/10597f220b047cee3e8ea50e91886d71.ico)" data-title="新浪">新浪</a>•<a class="sitelink sub-site" href="https://weibo.com/" data-title="微博">微博</a></div></li><li class="js_site-item site-item" data-id="3" data-title="搜狐" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/2a04dce430443d6593f2158e5ea83479.png" data-status="1" title="搜狐"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="http://www.sohu.com/" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/2a04dce430443d6593f2158e5ea83479.png)" data-title="搜狐">搜狐</a>•<a class="sitelink sub-site" href="http://tuijian.hao123.com/" data-title="热点">热点</a></div></li><li class="js_site-item site-item" data-id="4" data-title="腾讯" data-icon="https://gss2.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/5838ed1d6a3eef9f91341d9a8af16db8.ico" data-status="1" title="腾讯"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.qq.com/" style="background-image: url(https://gss2.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/5838ed1d6a3eef9f91341d9a8af16db8.ico)" data-title="腾讯">腾讯</a></div></li><li class="js_site-item site-item" data-id="5" data-title="网易" data-icon="https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/0243171b97e12fd795285d6603b199bb.ico" data-status="1" title="网易"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.163.com/" style="background-image: url(https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/0243171b97e12fd795285d6603b199bb.ico)" data-title="网易">网易</a></div></li><li class="js_site-item site-item" data-id="6" data-title="百度地图" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/bddt2018110949.png" data-status="1" title="百度地图"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://map.baidu.com/" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/bddt2018110949.png)" data-title="百度地图">百度地图</a></div></li><li class="js_site-item site-item" data-id="7" data-title="hao123影视" data-icon="https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png" data-status="1" title="hao123影视"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://v.hao123.baidu.com/" style="background-image: url(https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png)" data-title="hao123影视">hao123影视</a></div></li><li class="js_site-item site-item" data-id="8" data-title="免费游戏" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/game0331.png" data-status="1" title="免费游戏"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://game.hao123.com/" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/game0331.png)" data-title="免费游戏">免费游戏</a></div></li><li class="js_site-item site-item" data-id="9" data-title="凤凰网" data-icon="https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/d7fd0fcc2e428773bf1c105caa851de0.ico" data-status="1" title="凤凰网"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="https://www.ifeng.com/" style="background-image: url(https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/d7fd0fcc2e428773bf1c105caa851de0.ico)" data-title="凤凰网">凤凰网</a></div></li><li class="js_site-item site-item" data-id="10" data-title="天猫" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/10138.2.png" data-status="1" title="天猫"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="https://s.click.taobao.com/t?e=m%3D2%26s%3D7WCg0%2BpzKwgcQipKwQzePCperVdZeJviK7Vc7tFgwiFRAdhuF14FMa2XsNgKZ%2BOxt4hWD5k2kjP%2FTrTNBNETjAtOHPHN0vssKO4N%2F%2F7xLcVZMTj583r1vqUuZxIcp9pfUIgVEmFmgnaR4ypTBJBwtC8UTyjdhQwHJPwiig1bxLMnyi1UQ%2F17I10hO9fBPG8oXH%2BQH9e66Y4%3D" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/10138.2.png)" data-title="天猫">天猫</a>•<a class="sitelink sub-site" href="https://s.click.taobao.com/t?e=m%3D2%26s%3DAEbl0R9BF2IcQipKwQzePCperVdZeJviK7Vc7tFgwiFRAdhuF14FMYyfLH5Tv3XTJ1gyddu7kN%2F%2FTrTNBNETjAtOHPHN0vssHfUpkfuR0QZ9cgxTSFmAfKUuZxIcp9pfUIgVEmFmgnbDX0%2BHH2IEVa7A5ve%2FEYDnFveQ9Ld2jopwTqWNBsAwm%2BIKl4JSR4lzxgxdTc00KD8%3D" data-title="年中促">年中促</a></div></li><li class="js_site-item site-item" data-id="11" data-title="京东商城" data-icon="https://gss2.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/aa0448bf686b54f648b869155388d64e.ico" data-status="1" title="京东商城"><div class="inline-block-wrapper"><a class="sitelink icon-site g-red" href="https://union-click.jd.com/jdc?d=iEZf6v" style="background-image: url(https://gss2.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/aa0448bf686b54f648b869155388d64e.ico)" data-title="京东商城">京东商城</a></div></li><li class="js_site-item site-item" data-id="12" data-title="苏宁易购" data-icon="https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-09-18/7264782ab37241995f0f3ae65b2d0c86.png" data-status="1" title="苏宁易购"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="https://www.suning.com/?utm_source=hao123&amp;utm_medium=mingzhan" style="background-image: url(https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-09-18/7264782ab37241995f0f3ae65b2d0c86.png)" data-title="苏宁易购">苏宁易购</a></div></li><li class="js_site-item site-item" data-id="13" data-title="东方财富" data-icon="https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-12-12/30d4143e18a36bed146bb7e92e5a2464.png" data-status="1" title="东方财富"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.eastmoney.com/" style="background-image: url(https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-12-12/30d4143e18a36bed146bb7e92e5a2464.png)" data-title="东方财富">东方财富</a></div></li><li class="js_site-item site-item" data-id="14" data-title="淘宝网" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/a509892950a44d630d6fb5495ca07160.ico" data-status="1" title="淘宝网"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="https://www.taobao.com/" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/a509892950a44d630d6fb5495ca07160.ico)" data-title="淘宝网">淘宝网</a>•<a class="sitelink sub-site" href="http://redirect.simba.taobao.com/rd?c=un&amp;w=bd&amp;f=https%3A%2F%2Fmos.m.taobao.com%2Funion%2FxjkPC%3Fpid%3Dmm_26632322_6858406_107180550345&amp;k=552579a399777ebd&amp;p=mm_26632322_6858406_107180550345" data-title="爆品">爆品</a></div></li><li class="js_site-item site-item" data-id="15" data-title="爱奇艺" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/24c7e207a280974a518b1290a25bce4e.png" data-status="1" title="爱奇艺"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.iqiyi.com/" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/24c7e207a280974a518b1290a25bce4e.png)" data-title="爱奇艺">爱奇艺</a></div></li><li class="js_site-item site-item" data-id="16" data-title="聚划算" data-icon="https://gss3.bdstatic.com/5bVZsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/f9af92806a33df13df570b10af5aac61.ico" data-status="1" title="聚划算"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="https://s.click.taobao.com/JREwLKw" style="background-image: url(https://gss3.bdstatic.com/5bVZsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/f9af92806a33df13df570b10af5aac61.ico)" data-title="聚划算">聚划算</a><a monkey="tips_on" class="tips_link g_tips-r" alog-text="聚划算_提前开抢" href="https://s.click.taobao.com/zZ8FjFw" cls="ds,y" alog-custom="ind:ds,sal:1">&nbsp;<i class="g_icon">提前开抢</i></a></div></li><li class="js_site-item site-item" data-id="17" data-title="优酷网" data-icon="https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/106051.png" data-status="1" title="优酷网"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.youku.com/" style="background-image: url(https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/106051.png)" data-title="优酷网">优酷网</a></div></li><li class="js_site-item site-item" data-id="18" data-title="12306" data-icon="https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/hcp20180906.png" data-status="1" title="12306"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://www.12306.cn/" style="background-image: url(https://gss1.bdstatic.com/5bVXsj_p_tVS5dKfpU_Y_D3/urlicon/hcp20180906.png)" data-title="12306">12306</a></div></li><li class="js_site-item site-item" data-id="19" data-title="爱淘宝" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-07-10/16c593b3396fd2ed58ce6851ff76b2d0.png" data-status="1" title="爱淘宝"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://redirect.simba.taobao.com/rd?c=un&amp;w=bd&amp;f=https%3A%2F%2Fai.taobao.com%3Fpid%3Dmm_26632322_6858406_107180850312&amp;k=da998173fb03ba6a&amp;p=mm_26632322_6858406_107180850312" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-07-10/16c593b3396fd2ed58ce6851ff76b2d0.png)" data-title="爱淘宝">爱淘宝</a><a monkey="tips_on" class="tips_link g_tips-r" alog-text="爱淘宝_折上又折" href="http://redirect.simba.taobao.com/rd?c=un&amp;w=bd&amp;f=https%3A%2F%2Fmos.m.taobao.com%2Funion%2FPC618remai%3Fpid%3Dmm_43125636_4246598_107662750454&amp;k=6c846141454f20a1&amp;p=mm_43125636_4246598_107662750454" cls="ds,y" alog-custom="ind:ds,sal:1">&nbsp;<i class="g_icon">折上又折</i></a></div></li><li class="js_site-item site-item" data-id="20" data-title="58同城" data-icon="https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-11-11/331a6bbc2154a554b62b5bfce2d5cbd6.png" data-status="1" title="58同城"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://jump.luna.58.com/s?spm=b-31580022738699-me-f-862&amp;ch=mingzhan" style="background-image: url(https://gss0.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/res/r/image/2016-11-11/331a6bbc2154a554b62b5bfce2d5cbd6.png)" data-title="58同城">58同城</a></div></li><li class="js_site-item site-item" data-id="21" data-title="携程旅行网" data-icon="https://gss1.bdstatic.com/5eN1dDebRNRTm2_p8IuM_a/res/img/xiecheng20151019.png" data-status="1" title="携程旅行网"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://u.ctrip.com/union/CtripRedirect.aspx?TypeID=2&amp;Allianceid=1630&amp;sid=1911&amp;OUID=&amp;jumpUrl=http://www.ctrip.com/" style="background-image: url(https://gss1.bdstatic.com/5eN1dDebRNRTm2_p8IuM_a/res/img/xiecheng20151019.png)" data-title="携程旅行网">携程旅行网</a></div></li><li class="js_site-item site-item" data-id="22" data-title="网易云音乐" data-icon="https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/0243171b97e12fd795285d6603b199bb.ico" data-status="1" title="网易云音乐"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://music.163.com/" style="background-image: url(https://gss0.bdstatic.com/5bVSsj_p_tVS5dKfpU_Y_D3/qiusuo_icon/0243171b97e12fd795285d6603b199bb.ico)" data-title="网易云音乐">网易云音乐</a></div></li><li class="js_site-item site-item" data-id="23" data-title="Booking酒店" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-07-05/d89f23bc70874b09bf0ede1b13c3242e.png" data-status="1" title="Booking酒店"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="https://www.booking.com/index.html?aid=1337411" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2017-07-05/d89f23bc70874b09bf0ede1b13c3242e.png)" data-title="Booking酒店">Booking酒店</a></div></li><li class="js_site-item site-item" data-id="24" data-title="萌主页" data-icon="https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2019-02-28/ff749a82f16adede6b8d994ec67492e7.png" data-status="1" title="萌主页"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="http://moe.hao123.com/" style="background-image: url(https://gss0.bdstatic.com/5bVWsj_p_tVS5dKfpU_Y_D3/res/r/image/2019-02-28/ff749a82f16adede6b8d994ec67492e7.png)" data-title="萌主页">萌主页</a>•<a class="sitelink sub-site" href="http://v.hao123.com/dongman/" data-title="动漫">动漫</a></div></li><li class="js_site-item site-item" data-id="25" data-title="头条新闻" data-icon="https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png" data-status="1" title="头条新闻"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://tuijian.hao123.com/?type=rec" style="background-image: url(https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png)" data-title="头条新闻">头条新闻</a></div></li><li class="js_site-item site-item" data-id="26" data-title="体育" data-icon="https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/51619.png" data-status="1" title="体育"><div class="inline-block-wrapper"><a class="sitelink icon-site main-site" href="https://tuijian.hao123.com/sports" style="background-image: url(https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/51619.png)" data-title="体育">体育</a>•<a class="sitelink sub-site" href="https://www.baidu.com/s?word=NBA&amp;tn=50000014_hao_pg&amp;ie=utf-8" data-title="NBA">NBA</a></div></li><li class="js_site-item site-item" data-id="27" data-title="hao123旅游" data-icon="https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png" data-status="1" title="hao123旅游"><div class="inline-block-wrapper"><a class="sitelink icon-site" href="http://go.hao123.com/?tn=mz" style="background-image: url(https://gss0.bdstatic.com/5bVYsj_p_tVS5dKfpU_Y_D3/urlicon/1.1f32806366c6520864b669e487ec2ab8.png)" data-title="hao123旅游">hao123旅游</a></div></li></ul></div>
    '''

    content3 = "aac12 abbc112 adddc3332"

    # results = re.findall('<a.*href=.*?singer="(.*?)">(.*?)</a>', content, re.S)
    # results = re.findall('<li class="js_site-item site-item".*?data-title="(.*?)".*>(.*?)</a></div></li>', content2, re.S)
    results = re.findall('a(.*?)c(.*?)2', content3, re.S)
    # findall 返回 list
    print(results)
    print(type(results))
    for result in results:
        # result 是元组
        print(result)
        print(result[0], ' ', result[1])

def sub_test():
    content = 'hello1say2world5mine9'
    # sub 替换文本内的匹配正则的内容
    content = re.sub('\d+', ' ', content)
    print(content)

def compile_test():
    content1 = '2019-06-15 12:00'
    content2 = '2019-05-15 17:00'
    content3 = '2019-12-15 03:00'
    # 将 '\d{2}:\d{2}' 编译为正则表达式对象
    pattern = re.compile('\d{2}:\d{2}', re.S)
    result1 = re.sub(pattern, '', content1)
    result2 = re.sub(pattern, '', content2)
    result3 = re.sub(pattern, '', content3)
    print(result1, ' ', result2, ' ', result3)

if __name__ == '__main__':
    # match_test()
    # match_test2()
    # match_test3()
    # match_test4()
    # match_test5()
    # search_test()
    # findall_test()
    # sub_test()
    compile_test()
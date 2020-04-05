import requests
from Crypto.Cipher import AES
import base64
import json
import pymysql
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 获取音乐
songs_url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="  # post
comment_url_base = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_" # post

# 输出文件名称
out_put_file = 'wangyiyun.txt'
hot_comment_out_put_file = 'wangyiyun_hot.txt'
out_put_error_file = 'error.txt'

# mysql 链接   charset 设置为 utf8mb4 不要设置为 utf8 有些评论带表情，utf8 插入数据库会有warning
db = pymysql.connect(host="", user="", passwd="", db="db01", port=3306, charset='utf8mb4')

# es 链接
es = Elasticsearch(host='')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101'
                  ' Safari/537.36'
}

page_size = 100

class Comment:

    def __init__(self,comment_dict,songId, songName):
        # {"content":comment['content'],"likedCount":comment['likedCount'],"songId":song_id,"nickname":comment['user']['nickname']}
        self.__id__ = comment_dict['commentId']
        self.__content__ = comment_dict['content']
        self.__time__ = comment_dict['time']
        self.__likedCount__ = comment_dict['likedCount']
        self.__parentCommentId__ = comment_dict['parentCommentId']
        self.__nickname__ = comment_dict['user']['nickname']
        self.__userId__ = comment_dict['user']['userId']
        self.__songId__ = songId
        self.__songName__ = songName

    def __str__(self):
        return "id " + str(self.__id__) + " songName: " + self.__songName__ + " nickname: " + self.__nickname__ + " content: " + self.__content__ + \
               " likedCount: " + str(self.__likedCount__) + " time: " + str(self.__time__)

# 获取 每首歌的 评论
def get_comments(song_id, song_name):
    param = get_params(0)
    encSecKey = get_encSecKey()
    data = {
        "params": param,
        "encSecKey":encSecKey
    }
    # 每个歌曲的获取评论的 url
    comment_url = comment_url_base + str(song_id) + "?csrf_token="
    try:
        resp = requests.post(url=comment_url, data=data, headers=headers, timeout=10)
    except Exception as result:
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," 获取 %s 评论数量错误 " % song_name, result)
        write_error_to_file(" 获取 %s 评论数量错误 result %s" % (song_name, result))
    else:
        comment_json = resp.json()
        total = comment_json['total']

        # 热评  每首歌 15条 热评
        hot_comment_list_json = comment_json['hotComments']
        hot_comment_list = []
        for hot_comment in hot_comment_list_json:
            # com = {"content":comment['content'],"likedCount":comment['likedCount'],"songId":song_id,"nickname":comment['user']['nickname']}
            # 拼装对象
            com_obj = Comment(hot_comment, song_id, song_name)
            # 写入 本地文件
            hot_comment_write_to_file(com_obj.__str__())
            hot_comment_list.append(com_obj)
        if len(hot_comment_list) > 0:
            # 插入 mysql
            hot_batch_insert_mysql(hot_comment_list)

        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," 抓取 %s 的评论，一共 %d 条" % (song_name, total))
        flag = 0
        # 获取评论
        # for page in reversedrsed(rangege(int(total/page_size+1))):
        for page in range(int(total/page_size+1)):
            # 50 页 睡眠， 避免封 ip
            print("爬取 %s  第 %d 页"  % (song_name, page+1))
            if page % 10 == 0 and page > 50:
                print("睡眠中 %s %d " % (song_name, page+1))
                time.sleep(5)
            if page % 100 == 0 and page > 1000:
                print("睡眠中 %s %d " % (song_name, page+1))
                time.sleep(20)

            page_comment_list = get_page_comment_list(song_id, song_name, page, page_size)
            if page_comment_list is None or len(page_comment_list) == 0:
                write_error_to_file(" 抓取 %s 的评论，第 %d 页 数据为空" % (song_name, page))
                print(" 抓取 %s 的评论，第 %d 页 数据为空" % (song_name, page))
                break
            if page_comment_list is not None and len(page_comment_list) > 0:
                # mysql
                count = batch_insert_mysql(page_comment_list)
                # 如果插入的数据行数为0， 表示获取的评论为重复的
                if count == 0:
                    flag = flag +1
                    # 两次获取评论相同的话 则不继续爬取，
                    if flag == 2:
                        write_error_to_file(" 抓取 %s 的评论，第 %d 页" % (song_name, page))
                        break
                for comment in page_comment_list:
                    # print(comment)
                    write_to_file(comment.__str__())
                    # insert_mysql(comment)

# 分页获取 歌曲 的评论
def get_page_comment_list(song_id, song_name, page_num, pageSize):
    param = get_params(page_num, pageSize)
    encSecKey = get_encSecKey()
    data = {
        "params": param,
        "encSecKey": encSecKey
    }
    comment_url = comment_url_base + str(song_id) + "?csrf_token="
    try:
        resp = requests.post(url=comment_url, data=data, headers=headers,timeout=10)
    except Exception as result:
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," " + song_name, " 第 ",page_num, ' 页获取数据失败', result)
        write_error_to_file(" 歌曲 %s 第 %d 页获取数据失败 result %s" % (song_name ,page_num, result))
        return None
    else:
        comment_json = resp.json()
        comment_list_json = comment_json["comments"]
        comment_list = []
        for comment in comment_list_json:
            # com = {"content":comment['content'],"likedCount":comment['likedCount'],"songId":song_id,"nickname":comment['user']['nickname']}
            com_obj = Comment(comment,song_id,song_name)
            comment_list.append(com_obj)
        return comment_list

# 获取分页参数获取加密参数
def get_params(pageNum, pageSize = 20):
    if pageNum == 0:
        first_param = '{rid:"", offset:"0", total:"true", limit:' + str(pageSize) + ', csrf_token:""}'
    else:
        offset = str(pageNum * pageSize)
        # first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'flase')
        first_param = '{rid:"", offset:"%s", total:"%s", limit:' + str(pageSize) + ', csrf_token:""}'
        first_param = first_param % (offset, 'flase')
        print("first_param %s, pageNum %s, pageSize %s" % (first_param, pageNum, pageSize))
    # 这里是转为 二进制
    iv = b"0102030405060708"
    # 这里是转为 二进制
    first_key = b"0CoJUm6Qyw8W8jud"
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    # h_encText 是二进制， AES_encrypt() 第一参数需要 str ，所以把 h_encText 转为 str
    h_encText = AES_encrypt(h_encText.decode('utf-8'), bytes(second_key, encoding = "utf8")+b"", iv)
    return h_encText

def AES_encrypt(text, key, iv):
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encrypt_text = encryptor.encrypt(bytes(text, encoding = "utf8")+b"")
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

# 获取歌曲id及歌曲名称
def get_song_id():

    data = {
        # 许嵩的
        "params": "KcgvTSDue1viaYxe07Zd+TqT3aaJZ2CfQ0FIOySNGI2ouQnVRHTA2XN8v8+ydxOadocWof/DGCMpXNSAKEHMf0Y/HJlyG2soJ7WaefhCkr8mm0nSpX9nQjIVK9iIkpQ14Q2UXQht5JUmgKLlYuJJ2TdVmhaBtbl+K12v0JXqzl+l0DRQWovH2MvkrdhAhCWty3cRuSbu/dlbGU140HLTO5/pT7ZeTxcPe8/jB/txC/B1QnafGnAiFerXYHdn4N61benQ8TeSQNcFOgfUypNgoaiyh8nJy5OzvE5XYwtkh/7JMRbMIEB6vpp4FYnfNEBi",
        "encSecKey": "95a9dc4f10032b4db1a5e40bc78e8c5009130370cfa2412a3203aac932ebca7de3958d3a682be22aa521ab4408ed5d9e2d502dff9b5e2631386ff1ef161dff5e43e1fef1e356eea17dfaf4c444de0119504b383e0113a7b2b65b11d260b1f6b5a20df4394e04eac3ff75c9092f05f82b2e0ab8abb7c9156e0ccb5c9c5e1869b9"
    }

    # songs_url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101'
    #                   ' Safari/537.36'
    # }
    resp = requests.post(url=songs_url, data=data, headers=headers)
    # content = resp.content.decode()
    resp_json= resp.json()
    arr = resp_json['result']['songs']
    songs_id = []
    for song in arr:
        # print(song['id'], song['name'])
        id2name = {song['id']: song['name']}
        songs_id.append(id2name)
    return songs_id

# 写入文件
def write_to_file(content):
    with open(out_put_file, 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        # dumps实现字典的序列化  ensure_ascii=False 保证输出的是中文不是Unicode编码
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def hot_comment_write_to_file(content):
    with open(hot_comment_out_put_file, 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        # dumps实现字典的序列化  ensure_ascii=False 保证输出的是中文不是Unicode编码
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def write_error_to_file(content):
    with open(out_put_error_file, 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        # dumps实现字典的序列化  ensure_ascii=False 保证输出的是中文不是Unicode编码
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

# 写入数据库
def insert_mysql(comment):
    sql = "INSERT IGNORE INTO  " \
          "`yun_comment` (`id`, `song_id` ,`song_name`,`content`, `nick_name`, " \
          "`liked_count`, `parent_comment_id`, `user_id`, `time`, `create_date`) " \
          "VALUES ('%d', '%d', '%s', '%s', '%s', '%d', '%d', '%d', '%s','%d', now())"
    sql = sql % (comment.__id__,comment.__songId__,transferContent(comment.__songName__),transferContent(comment.__content__),transferContent(comment.__nickname__),
                 comment.__likedCount__,comment.__parentCommentId__,comment.__userId__,formate_time_to_date(comment.__time__),comment.__time__)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as result:
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," insert error sql: %s" % sql, result)
        write_error_to_file(" insert error sql: %s result %s" % (sql, result))

# 批量插入 mysql
def batch_insert_mysql(comment_list):
    sql = "INSERT IGNORE INTO `yun_comment` (`id`, `song_id` ,`song_name`,`content`, `nick_name`, " \
          "`liked_count`, `parent_comment_id`, `user_id`,`comment_date` ,`time`, `create_date`) VALUES "
    for i in range(len(comment_list)):
        comment = comment_list[i]
        sql += "('%d', '%d', '%s', '%s', '%s', '%d', '%d', '%d', '%s','%d', now())," % \
               (comment.__id__,comment.__songId__,transferContent(comment.__songName__),transferContent(comment.__content__),transferContent(comment.__nickname__),
                comment.__likedCount__,comment.__parentCommentId__,comment.__userId__,formate_time_to_date(comment.__time__),comment.__time__)
    sql = sql[:len(sql)-1]
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        # print("result %s , sql %s" % (result, sql))
        db.commit()
        return result
    except Exception as result:
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," insert error sql: %s, result:" % sql, result)
        write_error_to_file(" insert error sql: %s, result %s" %(sql, result))
        return 1

# 热评批量插入mysql
def hot_batch_insert_mysql(comment_list):
    sql = "INSERT IGNORE INTO `yun_comment_hot` (`id`, `song_id` ,`song_name`,`content`, `nick_name`, " \
          "`liked_count`, `parent_comment_id`, `user_id`, `comment_date`,`time`, `create_date`) VALUES "
    for i in range(len(comment_list)):
        comment = comment_list[i]
        sql += "('%d', '%d', '%s', '%s', '%s', " \
               "'%d', '%d', '%d', '%s','%d', now())," % \
               (comment.__id__,comment.__songId__,transferContent(comment.__songName__),
                transferContent(comment.__content__),transferContent(comment.__nickname__),
                comment.__likedCount__,comment.__parentCommentId__,comment.__userId__,formate_time_to_date(comment.__time__),comment.__time__)
    sql = sql[:len(sql)-1]
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        # print("result %s , sql %s" % (result, sql))
        db.commit()
        return result
    except Exception as result:
        print(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())) ," insert error sql: %s, result:" % sql, result)
        write_error_to_file(" insert error sql: %s, result %s" %(sql, result))
        return 1

# 转义字符
def transferContent(content):
    if content is None:
        return None
    else:
        string = ""
        for c in content:
            if c == "'":
                string += "\\\'"
            else:
                string += c
        return string

# time 转为 日期
def formate_time_to_date(timeStamp):
    timeStampStr = str(timeStamp)
    if len(timeStampStr) > 10:
        timeStampStr = timeStampStr[0:10]
    timeArray = time.localtime(int(timeStampStr))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def test_es():

    # 插入1条数据
    # body = {
    #     'id':2,
    #     'name':'test_02'
    # }
    # res = es.index(index='test_01',doc_type = 'json',id=2,body=body)
    # print(res)

    # 获取数据
    # getres = es.get(index='test_01',doc_type = 'json',id=12)
    getres = es.get(index='yun_music',doc_type = 'comment',id='_3218100629')
    count = es.count(index='yun_music',doc_type = 'comment')
    print(getres)
    print(count)

    # body = {
    #     "query": {
    #         "match_all": {
    #         }
    #     }
    # }
    # res = es.search(index='test_01',doc_type = 'json', body=body)
    # print(res)

    # 批量插入
    # action = []
    # action1 = {
    #     '_op_type': 'index',  # #操作 index update create delete
    #     '_index': 'test_01',
    #     '_type': 'json',
    #     '_source': {
    #         'id': 11,
    #         'name': 'test_11'
    #     }
    # }
    # action2 = {
    #     '_op_type': 'index',  # #操作 index update create delete
    #     '_index': 'test_01',
    #     '_type': 'json',
    #     '_id': 12,
    #     '_source': {
    #         'id': 12,
    #         'name': 'test_12'
    #     }
    # }
    # action.append(action1)
    # action.append(action2)
    # bulk_res = helpers.bulk(client=es, actions=action)
    # print(bulk_res)

def db_to_es():
    sql_count = "select count(*) from yun_comment"
    cursor = db.cursor()
    cursor.execute(sql_count)
    count = cursor.fetchone()[0]

    for page in range(int(count/page_size)+1):
        start = page_size * page
        sql = 'select * from yun_comment limit %d, %d ' %(start, page_size)
        # sql = 'select * from yun_comment limit 0,1 '
        cursor.execute(sql)
        comment_tuple = cursor.fetchall()
        print('第 %d 页数据, 当前组第一首歌曲 %s, %d' % ((page + 1), comment_tuple[0][2], comment_tuple[0][0]))
        action_list = []
        for comment in comment_tuple:
            action = {
                '_op_type': 'index',  # #操作 index update create delete
                '_index': 'yun_music',
                '_type': 'comment',
                '_id':'_'+str(comment[0]),
                '_source': {
                    'comment_id':comment[0],
                    'song_id':comment[1],
                    'song_name':comment[2],
                    'content':comment[3],
                    'nick_name':comment[4],
                    'liked_count':comment[5],
                    'comment_date':comment[6],
                    'user_id':comment[8],
                }
            }
            action_list.append(action)
        try :
            resp = helpers.bulk(client=es, actions=action_list)
        except Exception as ex:
            print('error : ', ex)
        else:
            print('resp : ', resp)

if __name__ == '__main__':
    t1 = time.time()
    print("开始时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    id2name = get_song_id()
    for song in id2name:
        for id,name in song.items():
            get_comments(id, name)
            print(id, name)
    print("结束时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    print("耗时 %d" % (time.time() - t1))

    # for page in reversed(range(10)):
    #     print(page)

    # test_es()

    # mysql  评论数据数据导入 es
    # t1 = time.time()
    # print("开始时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    # db_to_es()
    # print("结束时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    # print("耗时 %d" % (time.time() - t1))

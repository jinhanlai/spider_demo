# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.htmlcd
import pymysql
from twisted.enterprise import adbapi  # 用来做数据库处理的
from pymysql import cursors


class JianshuPipeline(object):
    def __init__(self):
        dbpara = {
            'user': 'root',
            'password': "",
            'port': 3306,
            "charset": "utf8mb4",
            "database": "jianshu"
        }
        self.conn = pymysql.connect(**dbpara)  # 两个**是因为把dbpare的参数解析成user=root这种形式
        self.cursor = self.conn.cursor()
        self._sql = None

    # 这个是同步插入到数据库，速度比较慢
    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author']
                                       , item['pub_time'], item['article_id'], item['head_portrait']
                                       , item['origin_urls']))
        self.conn.commit()
        return item

    # 将方法变成属性
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into detail(title,content,author,pub_time,
            article_id,head_portrait,origin_urls) values(%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


# 使用异步保存到数据库，用的是twisted中自带的ConnectionPool
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbpara = {
            'user': 'root',
            'password': "",
            'port': 3306,
            "charset": "utf8mb4",  # utf8mb4可以识别表情
            "database": "jianshu",
            "cursorclass": cursors.DictCursor  # 要导入一个游标的类
        }
        # 创建连接池
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbpara)
        self._sql = None

    # 将方法变成属性
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into detail(title,content,author,pub_time,
                article_id,head_portrait,origin_urls,like_count,subject) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'], item['author']
                                  , item['pub_time'], item['article_id'], item['head_portrait']
                                  , item['origin_urls'], item['like_count'], item['subject']))

    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(item['origin_urls'])
        print(item['subject'])
        print(item['title'])
        print(error)
        print('=' * 10 + 'error' + '=' * 10)
        # 存在：1406, "Data too long for column 'title' at row 1")错误
        # ：(1366, "Incorrect string value: '\\xF0\\x9F\\x93\\x9D,\\xE6...' for column 'subject' at row 1")
        #1366是字符出问题，不能识别表情这些

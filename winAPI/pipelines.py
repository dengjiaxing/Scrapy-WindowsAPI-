# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient
import pymongo

class WinapiPipeline(object):
    # def __init__(self):
    #     self.client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
    #     self.db = self.client[settings['MONGODB_DBNAME']]
    #     self.post = self.db[settings['MONGODB_DOCNAME']]
    def connect_db(self):  # 连接mongodb数据库
        client = MongoClient('localhost', 27017)
        db_name = 'test_api'
        db = client[db_name]
        collection_useraction = db['example']
        return collection_useraction
    def process_item(self, item, spider):
        #print item
        con = self.connect_db()
        con.insert( dict(item))


        # bookinfo = dict(item)
        # self.post.insert(bookinfo)
        # return item
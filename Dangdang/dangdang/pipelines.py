# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings
from .items import DangdangItem  # ,PicItem
settings = get_project_settings()


class DangdangPipeline(object):
    def __init__(self):
        host = settings['MYSQL_HOST']
        port = settings['MYSQL_PORT']
        db_name = settings['MYSQL_DBNAME']
        self.conn = pymysql.connect(host=host, port=port, user='root', password='123456789', database=db_name, charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT INTO book(title, comments, times, press, price, discount, category1, category2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"

    def process_item(self, item, spider):
        '''先判断itme类型，在放入相应数据库'''
        if isinstance(item, DangdangItem):
            try:
                self.cursor.execute(self.sql, (item["title"],item["comments"],item["times"],item["press"],
                                                 item["press"],item["price"],item["discount"],
                                                 item["category1"],item["category2"]))
                self.conn.commit()
            except Exception:
                pass
        # elif isinstance(item,PicItem):
        #     pass
        # try:
        #     PicItem   #
        # except Exception:
        #     pass
        return item

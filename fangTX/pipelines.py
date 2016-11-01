# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import ConfigParser
import sys
import hashlib
from fangTX.mysqlapi.mysql_connect import MySQLConnect
reload(sys)
sys.setdefaultencoding('utf-8')


class FangtxPipeline(object):

    def transformd5(self, url):
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()

    def save_to_sql(self, data):
        msq = MySQLConnect()
        data = json.loads(data)
        url_md5 = self.transformd5(data['url'])
        print type(data)
        print data
        sql = """
        insert into url_info_all_t (name, province, city, district, bizcircle, url, datatype, taskstatus, url_md5)
        values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');
        """ % (data['name'], data['provice'], data['city'], data['district'], data['bizcircle'], data['url'],
               data['datatype'], data['Taskstatus'], url_md5)
        print sql
        msq.insert_value(sql)

    def process_item(self, item, spider):
        config = ConfigParser.ConfigParser()
        config.read('./fangTX/city_conf.ini')
        config.get(spider.spidername, 'json_name')
        item = dict(item)
        f = codecs.open('./%s.json' % spider.spidername, 'a', encoding='utf-8')
        data = json.dumps(item, ensure_ascii=False)
        f.write(data + '\r\n')
        f.close()
        self.save_to_sql(data)
        return item

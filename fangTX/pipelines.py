# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class FangtxPipeline(object):

    def process_item(self, item, spider):
        print 'i am in piplines: ',
        print spider.spidername
        config = ConfigParser.ConfigParser()
        config.read('./fangTX/city_conf.ini')
        config.get(spider.spidername, 'json_name')
        item = dict(item)
        f = codecs.open('./%s.json' % spider.spidername, 'a', encoding='utf-8')
        data = json.dumps(item, ensure_ascii=False)
        f.write(data + '\r\n')
        f.close()
        return item

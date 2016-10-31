# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    provice = scrapy.Field()
    decorate_status = scrapy.Field()
    total_floor = scrapy.Field()
    site = scrapy.Field()
    house_orientation = scrapy.Field()
    total_price = scrapy.Field()
    xiaoqu_id = scrapy.Field()
    house_type = scrapy.Field()
    deal_time = scrapy.Field()
    city = scrapy.Field()
    pub_time = scrapy.Field()
    deal_status = scrapy.Field()
    name = scrapy.Field()
    idx = scrapy.Field()
    area = scrapy.Field()
    datatype = scrapy.Field()
    house_structure = scrapy.Field()
    floor = scrapy.Field()
    unit_price = scrapy.Field()
    url = scrapy.Field()
    house_year = scrapy.Field()


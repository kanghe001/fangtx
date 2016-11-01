#!/usr/bin/env python
# coding=utf-8

import logging
import scrapy
import ConfigParser
from fangTX.items import HubItem
logging.basicConfig(
    filemode='w',
    filename='./km.log',
    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class FangTXCrawl(scrapy.Spider):
    item = HubItem()
    name = 'fangtx'
    all_url = set([])

    def __init__(self, spider_name):
        self.config = ConfigParser.ConfigParser()
        self.config.read('./fangTX/city_conf.ini')
        super(FangTXCrawl, self).__init__()
        self.spidername = spider_name
        self.start_urls = (
            self.config.get(self.spidername, 'start_url'),
        )

    def parse(self, response):
        print 'i am in parse'
        qy_part_url = response.xpath('//div[@class="qxName"]/a')[1:]
        for url in qy_part_url:
            complete_qy_url = response.urljoin(url.xpath('@href').extract_first())
            logging.debug('complete_qy_url: %s' % complete_qy_url)
            yield scrapy.Request(complete_qy_url, callback=self.get_sub_area)

    def get_sub_area(self, response):
        sub_area_list = response.xpath('//p[@id="shangQuancontain"]/a')[1:]
        for sub_area in sub_area_list:
            sub_area_url = sub_area.xpath('@href').extract_first()
            sub_area_url_full = response.urljoin(sub_area_url)
            logging.debug('sub_area_url: %s' % sub_area_url)
            yield scrapy.Request(sub_area_url_full, callback=self.get_page_num)

    def get_page_num(self, response):
        house_num = response.xpath('//b[@class="org"]/text()').extract_first()
        num_per_page = len(response.xpath('//div[@class="houseList"]/dl'))
        if not num_per_page:
            return
        page_num = int(house_num) / num_per_page
        yushu = int(house_num) % num_per_page
        if yushu:
            page_num += 1
        for i in range(1, page_num+1):
            next_page = response.url + 'i3' + str(i) + '/'
            print 'next_page: ' + next_page
            yield scrapy.Request(next_page, callback=self.get_house_url)

    def get_house_url(self, response):
        house_url_list = response.xpath('//div[@class="houseList"]/dl')
        for house in house_url_list:
            house_url = house.xpath('dd/p[1]/a/@href').extract_first()
            house_detail_url = response.urljoin(house_url)
            logging.debug('house_detail_url: %s' % house_detail_url)
            self.item['url'] = house_detail_url

            name = house.xpath('dd/p[1]/a/text()').extract_first()
            if name:
                self.item['name'] = name.split()[0]
            else:
                self.item['name'] = name
            self.item['district'] = house.xpath('dd/p[3]/a[1]/text()').extract_first()
            self.item['bizcircle'] = house.xpath('dd/p[3]/a[2]/text()').extract_first()
            self.item['datatype'] = self.config.get(self.spidername, 'datatype')
            self.item['provice'] = self.config.get(self.spidername, 'provice')
            self.item['city'] = self.config.get(self.spidername, 'city')
            self.item['Taskstatus'] = self.config.get(self.spidername, 'Taskstatus')
            yield self.item

'''
    def house_info(self, response):
        if response.url not in self.all_url:
            self.all_url.add(response.url)
        else:
            return

        info_part = response.xpath('//div[@id="chengjiaoxq_B02_02"]')
        item = FangtxItem()
        item['total_floor'] = info_part.xpath('div/p[2]/text()').extract_first()
        item['house_orientation'] = info_part.xpath('ul/li[3]/p[2]/b/text()').extract_first()
        item['total_price'] = info_part.xpath('ul/li[1]/p[2]/b/text()').extract_first()
        item['floor'] = info_part.xpath('div/p[2]/text()').extract_first()
        item['unit_price'] = info_part.xpath('ul/li[2]/p[2]/b/text()').extract_first()
        item['house_year'] = None
        item['house_structure'] = response.xpath('//div[@class="title title1"]/h1/text()').extract_first()
        item['name'] = info_part.xpath('div/p[3]/a[1]/text()').extract_first()
        item['idx'] = info_part.xpath('div/p[3]/a[1]/text()').extract_first()
        item['area'] = info_part.xpath('div/p[1]/text()').extract_first()
        item['xiaoqu_id'] = info_part.xpath('div/p[3]/a[1]/text()').extract_first()
        item['deal_time'] = response.xpath('//div[@class="title title1"]/h1/span/text()').re_first('\d*-*\d*-*\d*')
        item['url'] = response.url
        item['datatype'] = self.config.get(self.spidername, 'datatype')
        item['provice'] = self.config.get(self.spidername, 'provice')
        item['site'] = self.config.get(self.spidername, 'site')
        item['house_type'] = self.config.get(self.spidername, 'house_type')
        item['city'] = self.config.get(self.spidername, 'city')
        item['pub_time'] = self.config.get(self.spidername, 'pub_time')
        item['deal_status'] = self.config.get(self.spidername, 'deal_status')
        yield item
'''




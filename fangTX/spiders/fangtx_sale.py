#!/usr/bin/env python
# coding=utf-8

import logging
import scrapy
import threading
import ConfigParser
from fangTX.items import HubItem
lock = threading.Lock()
logging.basicConfig(
    filemode='w',
    filename='./fz_fang_sale.log',
    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class FangTXCrawl(scrapy.Spider):
    item = HubItem()
    name = 'fangtx_sale'
    all_url = set([])
    second_url = []

    def __init__(self, spider_name):
        self.config = ConfigParser.ConfigParser()
        self.config.read('./fangTX/city_conf.ini')
        super(FangTXCrawl, self).__init__()
        self.spidername = spider_name
        self.start_urls = (
            self.config.get(self.spidername, 'start_url'),
        )

    def parse(self, response):
        start = self.config.getint(self.spidername, 'qystart')
        qy_part_url = response.xpath(self.config.get(self.spidername, 'qy_part_url'))[start:]
        for url in qy_part_url:
            complete_qy_url = response.urljoin(url.xpath('@href').extract_first())
            complete_qy_name = response.urljoin(url.xpath('text()').extract_first())
            logging.debug('complete_qy_url: %s' % complete_qy_url)
            logging.debug('complete_qy_name: %s' % complete_qy_name)
            yield scrapy.http.Request(complete_qy_url, callback=self.get_sub_area)

    def get_sub_area(self, response):
        start = self.config.getint(self.spidername, 'sub_area_start')
        print 'start: ', start, type(start)
        sub_area_list = response.xpath(self.config.get(self.spidername, 'sub_area_list'))[start:]
        for sub_area in sub_area_list:
            sub_area_url = sub_area.xpath('@href').extract_first()
            sub_area_name = sub_area.xpath('text()').extract_first()
            sub_area_url_full = response.urljoin(sub_area_url)
            logging.debug('sub_area_url_full: %s' % sub_area_url_full)
            logging.debug('sub_area_name: %s' % sub_area_name)
            yield scrapy.http.Request(sub_area_url_full, callback=self.get_price)

    def get_price(self, response):
        logging.debug('i am in get_price')
        price_part_url = response.xpath('//li[@id="list_D02_11"]/p/a/@href').extract()[1:]
        for price in price_part_url:
            logging.debug('price: %s' % price)
            price_url_full = response.urljoin(price)
            yield scrapy.Request(price_url_full, callback=self.get_page_num, dont_filter=True)

    def get_page_num(self, response, time=1):
        page_num = response.xpath(self.config.get(self.spidername, 'house_num_xpath')).re_first('\d+/(\d+)')
        # yushu = int(house_num) % num_per_page
        # print 'yushu: ', yushu
        # if yushu:
        #   page_num += 1
        if not page_num:
            if time == 1:
                logging.debug('times come here: %s' % time)
                yield scrapy.Request(response.url,
                callback=lambda response=response, time=time + 1: self.get_page_num(response, time), dont_filter=True)
            return
        page_num = int(page_num)
        logging.debug('page_num: %s' % page_num)

        for i in range(1, page_num+1):
            next_page = response.url[:-1] + '-i3' + str(i) + '/'
            logging.debug('next_page: %s' % next_page)
            yield scrapy.http.Request(next_page, callback=self.get_house_url)

    def get_house_url(self, response, time=1):
        house_url_list = response.xpath(self.config.get(self.spidername, 'house_url_list_xpath'))
        if not house_url_list and time == 1:
            logging.debug('times come here: %s' % time)
            yield scrapy.Request(response.url,
                callback=lambda response=response, time=time: self.get_house_url(response, time+1), dont_filter=True)
        logging.debug('times come here: %s' % time)
        logging.debug('num_per_page_true: %s' % len(house_url_list))
        for house in house_url_list:
            house_url = house.xpath(self.config.get(self.spidername, 'house_url')).extract_first()
            house_detail_url = response.urljoin(house_url)
            logging.debug('house_page_url: %s' % response.url)
            logging.debug('house_detail_url: %s' % house_detail_url)
            self.item['url'] = house_detail_url

            name = house.xpath(self.config.get(self.spidername, 'name')).extract_first()
            if name:
                self.item['name'] = name.split()[0]
            else:
                self.item['name'] = name
            logging.debug('house_name: %s' % self.item['name'])
            self.item['district'] = response.xpath(self.config.get(self.spidername, 'district')).extract_first()
            self.item['bizcircle'] = response.xpath(self.config.get(self.spidername, 'bizcircle')).extract_first()
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




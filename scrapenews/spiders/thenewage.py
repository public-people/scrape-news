# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ThenewageSpider(CrawlSpider):
    name = 'thenewage'
    allowed_domains = ['www.thenewage.co.za']
    start_urls = ['http://www.thenewage.co.za/']

    rules = (Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),)

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

# -*- coding: utf-8 -*-
import scrapy


class ThenewageSpider(scrapy.Spider):
    name = 'thenewage'
    allowed_domains = ['www.thenewage.co.za']
    start_urls = ['http://www.thenewage.co.za/']

    def parse(self, response):
        pass

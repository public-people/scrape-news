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
        title = response.xpath('//h1[contains(@class, "entry-title")]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'activity':
            body_html = response.xpath('//div[contains(@class, "td-post-content")]').extract_first()
            self.logger.info(body_html)
        self.logger.info("")

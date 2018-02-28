# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem


class ThenewageSpider(CrawlSpider):
    name = 'thenewage'
    allowed_domains = ['www.thenewage.co.za']
    start_urls = ['http://www.thenewage.co.za/']

    rules = (Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),)

    publication_name = 'The New Age'

    def parse_item(self, response):
        title = response.xpath('//h1[contains(@class, "entry-title")]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'activity':
            body_element = response.xpath('//div[contains(@class, "td-post-content")]')
            body_html = body_element.extract_first()
            byline = body_element.xpath('//p[last()]/text()').extract_first()
            publication_date = response.xpath('//time/@datetime').extract_first()

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['publication_date'] = publication_date
            item['url'] = response.url
            item['publication_name'] = self.publication_name

            yield item
        self.logger.info("")

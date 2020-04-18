# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import re


class encaSpider(CrawlSpider):
    name = 'enca'
    allowed_domains = ['www.enca.com']
    start_urls = ['https://www.enca.com/news-stream/south-africa']

    link_extractor = LinkExtractor(allow=('/south-africa'))
    rules = (
        Rule(link_extractor, callback='parse_item', follow=True),
    )

    publication_name = 'eNCA'

    def parse_item(self, response):
        title = response.css('header.article-header h1').xpath('text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        
        publication_date = response.css('.article-meta time').xpath('@datetime').extract_first()
        body_html = response.css('.article-text').extract_first()

        if body_html:
            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['published_at'] = publication_date
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-1]
            item['publication_name'] = self.publication_name
            item['spider_name'] = self.name

            yield item
        else:
            self.logger.info("No body found for %s", response.url)

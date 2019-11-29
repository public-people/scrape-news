# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews.items import ScrapenewsItem


class ThenewageSpider(CrawlSpider):
    name = 'thenewage'
    allowed_domains = ['www.thenewage.co.za']
    start_urls = ['https://thenewage.co.za/']

    link_extractor = LinkExtractor(allow=())
    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'The New Age'

    def parse_item(self, response):
        title = response.xpath('//h1[contains(@class, "entry-title")]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'activity':
            body_element = response.xpath('//div[contains(@class, "td-post-content")]')
            body_html = body_element.extract_first()
            publication_date = response.xpath('//time/@datetime').extract_first()

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

    def filter_links(self, links):
        for link in links:
            match = re.search(r'/page/(\d+)/', link.url)
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif link.url.endswith('/home'):
                self.logger.info("Ignoring %s", link.url)
                continue
            elif match and int(match.groups(1)[0]) > 10:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

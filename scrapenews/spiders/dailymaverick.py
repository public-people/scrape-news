# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DailMaverickSpider(CrawlSpider):
    name = 'dailymaverick'
    allowed_domains = ['www.dailymaverick.co.za']
    start_urls = ['https://www.dailymaverick.co.za']

    link_extractor = LinkExtractor(allow=())
    rules = (
        Rule(link_extractor, callback='parse_item', follow=True),
    )

    publication_name = 'Daily Maverick'

    def parse_item(self, response):
        if '/opinionistas' in response.url:
            self.logger.info("Ignoring %s", response.url)
            return

        title = response.xpath('//div[@id="article"]/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//div[@id="article"]//div[contains(@class, "body")]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//meta[@name="author"]/@content').extract_first()
            publication_date_str = response.xpath('//meta[@name="published"]/@content').extract_first()

            publication_date = datetime.strptime(publication_date_str, '%Y-%m-%d')
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-2]
            item['spider_name'] = self.name

            item['publication_name'] = self.publication_name

            yield item

# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class News24Spider(CrawlSpider):
    name = 'news24'
    allowed_domains = ['www.news24.com']
    start_urls = ['https://www.news24.com']

    link_extractor = LinkExtractor(allow=())
    rules = (
        Rule(link_extractor, callback='parse_item', follow=True),
    )

    publication_name = 'News24'

    def parse_item(self, response):
        if '/News/' not in response.url:
            self.logger.info("Ignoring %s", response.url)
            return

        title = response.xpath('//div[contains(@class, "article_details")]/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//article[@id="article-body"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//div[contains(@class, "ByLineWidth")]/p/text()').extract_first()
            publication_date_str = response.xpath('//span[@id="spnDate"]/text()').extract_first()
            accreditation = response.xpath('//div[contains(@class, "ByLineWidth")]/div[contains(@class, "accreditation")]/a/@href').extract_first()

            publication_date = datetime.strptime(publication_date_str, '%Y-%m-%d %H:%M')
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-1]
            item['spider_name'] = self.name

            item['publication_name'] = self.publication_name
            if accreditation:
                item['publication_name'] += " with " + accreditation[1:]

            yield item
        self.logger.info("")

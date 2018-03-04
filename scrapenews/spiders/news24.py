# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem


class News24Spider(CrawlSpider):
    name = 'news24'
    allowed_domains = ['www.news24.com', 'localhost']
    start_urls = ['https://www.news24.com', "http://localhost:8888/Ramaphosa's headaches _ News24.html"]

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
            publication_date = response.xpath('//span[@id="spnDate"]/text()').extract_first()
            accreditation = response.xpath('//div[contains(@class, "ByLineWidth")]/div[contains(@class, "accreditation")]/a/@href').extract_first()

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['publication_date'] = publication_date
            item['url'] = response.url

            item['publication_name'] = self.publication_name
            if accreditation:
                item['publication_name'] += " with " + accreditation.extract_first()[1:]

            yield item
        self.logger.info("")

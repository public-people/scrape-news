# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem


class ThenewageSpider(CrawlSpider):
    name = 'thenewage'
    allowed_domains = ['www.news24.com']
    start_urls = ['https://www.news24.com']

    link_extractor = LinkExtractor(allow=())
    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'News24'

    def parse_item(self, response):
        title = response.xpath('//div[contains(@class, "article_details")]/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//article[contains(@class, "article-body")]')
        if article_body:
            body_html = article_body.extract_first()
            byline = body_element.xpath('//div[contains(@class, "ByLineWidth")]/p/text()').extract_first()
            publication_date = response.xpath('//span[contains(@class, spnDate)]/text()').extract_first()
            accreditation = body_element.xpath('//div[contains(@class, "ByLineWidth")]/div[contains(@class, "accreditation")]/a/@href')


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

    def filter_links(self, links):
        for link in links:
            if not '/News/' in link.url
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

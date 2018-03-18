# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class IOLSpider(CrawlSpider):
    name = 'iol'
    allowed_domains = ['www.iol.co.za']
    start_urls = ['https://www.iol.co.za']

    link_extractor = LinkExtractor(allow=())
    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'IOL News'

    def parse_item(self, response):

        title = response.xpath('//header/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//div[@itemprop="articleBody"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//span[@itemprop="author"]/strong/text()').extract_first()
            publication_date_str = response.xpath('//span[@itemprop="datePublished"]/@content').extract_first()

            publication_date = datetime.strptime(publication_date_str, '%Y-%m-%dT%H:%M')
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

            yield item

    def filter_links(self, links):
        for link in links:
            if '/news/eish' in link.url:
                self.logger.debug("Ignoring %s", link.url)
                continue
            elif '/news/opinion' in link.url:
                self.logger.debug("Ignoring %s", link.url)
                continue
            elif 'iol.co.za/news' in link.url:
                yield link
            else:
                self.logger.debug("Ignoring %s", link.url)

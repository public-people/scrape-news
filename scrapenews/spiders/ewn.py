# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews.items import ScrapenewsItem
from scrapenews import lib


SAST = pytz.timezone('Africa/Johannesburg')


class ewnSpider(CrawlSpider):
    name = 'ewn'
    allowed_domains = ['ewn.co.za']

    start_urls = ['http://ewn.co.za']

    link_extractor = LinkExtractor(
        allow=(r'http://ewn.co.za/[0-9]{4}/[0-9]{2}/[0-9]{2}/',),
        deny=()
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Eyewitness News'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.css('h2 > span').xpath('text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            body_html = " ".join(response.css('article.article-full p').extract())
            byline = response.css('.byline span[itemprop="author"] a ::text').extract_first()

            publication_date_str = response.xpath('//meta[@itemprop="datePublished"]/@content').extract_first()
            # alas no time portion: possibly use timelib to
            publication_date = lib.parse_date(publication_date_str)
            # datetime.datetime(2018, 6, 14, 11, 0)
            publication_date = SAST.localize(publication_date)
            # datetime.datetime(2018, 6, 14, 11, 0, tzinfo=<DstTzInfo 'Africa/Johannesburg' SAST+2:00:00 STD>)

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title
                item['byline'] = byline
                item['published_at'] = publication_date.isoformat()
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/').pop()
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

                yield item
            else:
                self.logger.info("No body found for %s", response.url)
                # should we be using canonical_url instead of response.url for the above?

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            yield link

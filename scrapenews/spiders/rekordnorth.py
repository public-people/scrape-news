# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews import lib
from scrapenews.items import ScrapenewsItem


SAST = pytz.timezone('Africa/Johannesburg')


class dfaSpider(CrawlSpider):
    name = 'rekordnorth'
    allowed_domains = ['rekordnorth.co.za']
    start_urls = ['https://rekordnorth.co.za/category/news-headlines/local-news/']

    article_link_extractor = LinkExtractor(
        allow=(r'https://rekordnorth.co.za/\d+/', ),
        allow_domains=allowed_domains
    )
    category_link_extractor = LinkExtractor(
        allow=('https://rekordnorth.co.za/category/', ),
        allow_domains=allowed_domains,
        deny='opinion-edition|lifestyle-news'
    )

    rules = (
        Rule(article_link_extractor, callback='parse_item', follow=True),
        Rule(category_link_extractor, follow=True),
    )

    publication_name = 'Rekord Pretoria-North'

    def parse_item(self, response):
        # Whitelist categories that are actually news
        if not response.css('.post-categories').xpath('li/a[contains(@href, "news-headlines")]'):
            self.logger.info("Skipping non-news article %s", response.url)
            return

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            article_body = response.css('div.entry-content')
            body_html = article_body.extract_first()
            byline = response.css('div.author-name').css('::text').extract_first()

            publication_date_str = response.xpath('//time/@datetime').extract_first()
            # u'2018-06-14T11:00:00+00:00'
            publication_date = lib.parse_date_hour_min_sec(publication_date_str)
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
                item['file_name'] = response.url.split('/')[-2]
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

                yield item
            else:
                self.logger.info("No body found for %s", canonical_url)

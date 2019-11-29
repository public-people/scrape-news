# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytz
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews import lib
from scrapenews.items import ScrapenewsItem


SAST = pytz.timezone('Africa/Johannesburg')


class sabcSpider(CrawlSpider):
    name = 'sabc'
    allowed_domains = ['sabcnews.com']

    start_urls = ['http://www.sabcnews.com/sabcnews/']

    link_extractor = LinkExtractor(
        allow=('http://www.sabcnews.com/sabcnews/', ),
        deny=(
            '/?post_type=',
            '/?p=',
            '/author/',
            '/feed/',
            '/rss-feeds/',
            '/tag/',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'SABC News'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()

        if og_type == 'article':
            article_body = response.css('div.post-content')
            body_html = " ".join(article_body.css('::text').extract())
            byline = response.css('span.author::text').extract_first().strip()

            # Ignore the first line which is a comment.
            publication_date_str = response.xpath('//span[@class="create"]/text()').extract()[1]
            publication_date = lib.parse_long_month_hour_min_meridian(publication_date_str)
            publication_date = SAST.localize(publication_date)

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title.strip()
                item['byline'] = byline
                item['published_at'] = publication_date.isoformat()
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/')[-2]
                # should we be using canonical_url instead of response.url for the above?
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
            else:
                yield link

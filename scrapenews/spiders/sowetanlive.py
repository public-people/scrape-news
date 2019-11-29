# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytz
from datetime import datetime

from scrapenews.items import ScrapenewsItem
from .sitemap import SitemapSpider


SAST = pytz.timezone('Africa/Johannesburg')


class SowetanliveSpider(SitemapSpider):
    name = 'sowetanlive'
    allowed_domains = ['www.sowetanlive.co.za']

    sitemap_urls = ['https://www.sowetanlive.co.za/robots.txt']
    sitemap_follow = [
        'www.sowetanlive.co.za/sitemap/anc-conference-2017/',
        'www.sowetanlive.co.za/sitemap/business/',
        'www.sowetanlive.co.za/sitemap/news/',
        'www.sowetanlive.co.za/sitemap/opinion/',
    ]

    publication_name = 'Sowetan Live'

    def parse(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1/span/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        article_body = response.css('div.article-widget-text')

        if article_body:
            body_html = " ".join(article_body.css('::text').extract())
            byline = response.css('span.article-author').xpath('@data-author').extract_first()

            publication_date_str = response.css('span.article-pub-date::text').extract_first().strip()
            # u'26 June 2018 - 07:28'
            publication_date = datetime.strptime(publication_date_str, '%d %B %Y - %H:%M')
            # datetime.datetime(2018, 6, 26, 7, 28)
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = canonical_url
            item['file_name'] = response.url.split('/')[-2]
            # should we be using canonical_url instead of response.url for the above?
            item['spider_name'] = self.name
            item['publication_name'] = self.publication_name

            yield item

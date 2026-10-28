# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class TimesliveSpider(SitemapSpider):
    name = 'timeslive'
    allowed_domains = ['www.timeslive.co.za']

    sitemap_urls = ['https://www.timeslive.co.za/arc/outboundfeeds/sitemap-news-index/']
    sitemap_rules = [
        (r'/news/', 'parse'),
        (r'/politics/', 'parse'),
        (r'/investigations/', 'parse'),
        (r'/opinion/', 'parse'),
    ]

    publication_name = 'Times Live'

    def parse(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url

        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        article_body = response.css('.b-article-body')
        if not article_body:
            self.logger.info("No body found for %s", response.url)
            return

        body_html = article_body.get()

        byline = response.css('.b-author-bio__author-name::text').get()
        if not byline:
            byline = response.css('meta[name=author]::attr(content)').get()

        publication_date_str = response.css('time[datetime]::attr(datetime)').get()
        if publication_date_str:
            publication_date = datetime.fromisoformat(publication_date_str)
            publication_date = publication_date.astimezone(SAST)
        else:
            publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

        item = ScrapenewsItem()
        item['body_html'] = body_html
        item['title'] = title.strip() if title else ''
        item['byline'] = byline.strip() if byline else ''
        item['published_at'] = publication_date.isoformat()
        item['retrieved_at'] = datetime.utcnow().isoformat()
        item['url'] = canonical_url
        item['file_name'] = response.url.split('/')[-2]
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item

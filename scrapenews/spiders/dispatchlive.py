# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from scrapenews.items import ScrapenewsItem
from .sitemap import SitemapSpider

SAST = pytz.timezone('Africa/Johannesburg')


class DispatchLiveSpider(SitemapSpider):
    name = 'dispatchlive'
    allowed_domains = ['www.dispatchlive.co.za']

    sitemap_urls = ['https://www.dispatchlive.co.za/robots.txt']
    sitemap_follow = [
        'www.dispatchlive.co.za/sitemap/news/',
        'www.dispatchlive.co.za/sitemap/politics/',
        'www.dispatchlive.co.za/sitemap/local-heroes/',
    ]

    publication_name = 'Dispatch Live'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()

        title = response.xpath('//h1/span/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('div.text')
        if article_body:
            # join multiple text sections
            body_html = " ".join(article_body.extract())
            byline = response.css('span.article-author').xpath('span/text()').extract_first()

            publication_date_str = response.css('span.article-pub-date::text').extract_first().strip()
            # '30 August 2018'
            publication_date = datetime.strptime(publication_date_str, '%d %B %Y')
            # datetime.datetime(2018, 8, 30, 0, 0)

            publication_date = SAST.localize(publication_date)

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

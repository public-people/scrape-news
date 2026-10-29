# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DispatchLiveSpider(SitemapSpider):
    name = 'dispatchlive'
    allowed_domains = ['dailydispatch.co.za']

    sitemap_urls = ['https://dailydispatch.co.za/sitemap.xml']
    sitemap_rules = [
        (r'/news/', 'parse'),
        (r'/politics/', 'parse'),
    ]

    publication_name = 'Dispatch Live'

    def parse(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url

        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('article')
        if article_body:
            body_html = article_body.get()
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
        else:
            self.logger.info("No body found for %s", response.url)

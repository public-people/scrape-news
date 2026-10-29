# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DailMaverickSpider(SitemapSpider):
    name = 'dailymaverick'
    allowed_domains = ['www.dailymaverick.co.za']

    sitemap_urls = ['https://www.dailymaverick.co.za/news-sitemap.xml']

    publication_name = 'Daily Maverick'

    def parse(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url

        if '/opinionistas' in canonical_url:
            self.logger.info("Ignoring %s", canonical_url)
            return

        title = response.css('h1::text').get()
        self.logger.info('%s %s', canonical_url, title)
        article_body = response.css('.article-container')
        if article_body:
            body_html = article_body.get()
            byline = response.css('meta[name=author]::attr(content)').get()
            publication_date_str = response.css('meta[name=published]::attr(content)').get()

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

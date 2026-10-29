# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz
import json

SAST = pytz.timezone('Africa/Johannesburg')


class IOLSpider(SitemapSpider):
    name = 'iol'
    allowed_domains = ['iol.co.za']

    sitemap_urls = ['https://iol.co.za/sitemap/']
    sitemap_rules = [
        (r'/news/', 'parse'),
        (r'/politics/', 'parse'),
        (r'/business-report', 'parse'),
        (r'/personal-finance', 'parse'),
        (r'/crime-and-courts', 'parse'),
    ]

    publication_name = 'IOL News'

    def parse(self, response):
        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        article_body = response.css('[class*=article_]')
        if not article_body:
            article_body = response.css('article')
        if not article_body:
            self.logger.info("No body found for %s", response.url)
            return

        body_html = article_body.get()

        byline = None
        publication_date = None
        for script in response.css('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.css('::text').get(''))
                if data.get('@type') == 'NewsArticle':
                    date_str = data.get('datePublished')
                    if date_str:
                        publication_date = datetime.fromisoformat(date_str)
                        publication_date = publication_date.astimezone(SAST)
                    authors = data.get('author', [])
                    if authors:
                        if isinstance(authors, dict):
                            byline = authors.get('name', '')
                        elif isinstance(authors, list):
                            byline = ', '.join(a.get('name', '') for a in authors if a.get('name'))
                    break
            except (json.JSONDecodeError, ValueError):
                continue

        if not byline:
            byline = response.css('meta[name=author]::attr(content)').get()
        if not publication_date:
            publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

        item = ScrapenewsItem()
        item['body_html'] = body_html
        item['title'] = title.strip() if title else ''
        item['byline'] = byline.strip() if byline else ''
        item['published_at'] = publication_date.isoformat()
        item['retrieved_at'] = datetime.utcnow().isoformat()
        item['url'] = response.url
        item['file_name'] = response.url.split('/')[-1]
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item

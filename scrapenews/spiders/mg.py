# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz
from w3lib.html import remove_tags

SAST = pytz.timezone('Africa/Johannesburg')

SKIP_STRINGS = [
    '\u00a9',     # copyright
    '\u2011',     # NON-BREAKING HYPHEN
    '\u2012',     # FIGURE DASH
    '\u2013',     # EN DASH
    '\u2014',     # EM DASH
    '\u2015',     # HORIZONTAL BAR
    'Agence France-Presse',
    'AFP',
    'Sapa',
    'Reuters',
    'I-Net Bridge',
    'Guardian News',
    'guardian.co.uk',
]

IGNORE_SECTIONS = [
    'world',
    'sport',
]


class MGSpider(SitemapSpider):
    name = 'mg'
    allowed_domains = ['mg.co.za']

    sitemap_urls = ['https://mg.co.za/sitemap.xml']

    sitemap_rules = [
        (r'/news/', 'parse'),
        (r'/politics/', 'parse'),
        (r'/business/', 'parse'),
        (r'/health/', 'parse'),
        (r'/education/', 'parse'),
        (r'/friday/', 'parse'),
        (r'/thought-leader/', 'parse'),
    ]

    publication_name = 'Mail & Guardian'

    def parse(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url

        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        article_body = response.css('article')
        if not article_body:
            self.logger.info("No body found for %s", response.url)
            return

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
        item['file_name'] = response.url.split('/')[-1]
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item

# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz
from w3lib.html import remove_tags

SAST = pytz.timezone('Africa/Johannesburg')

SKIP_STRINGS = [
    '\xc2\xa9', # copyright
    '\xe2\x80\x91', # NON-BREAKING HYPHEN
    '\xe2\x80\x92', # FIGURE DASH
    '\xe2\x80\x93', #EN DASH
    '\xe2\x80\x94', # EM DASH
    '\xe2\x80\x95', # HORIZONTAL BAR
    'Agence France-Presse',
    'AFP',
    'Sapa',
    'Reuters',
    'I-Net Bridge',
    'Guardian News',
    'guardian.co.uk',
]


class MGSpider(SitemapSpider):
    name = 'mg'
    allowed_domains = ['mg.co.za']

    sitemap_urls = ['https://mg.co.za/robots.txt']

    sitemap_follow = [
        '/sitemaps/',
    ]

    sitemap_rules = [
        ('mg.co.za/article', 'parse'),
    ]

    publication_name = 'Mail & Guardian'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        publication_date_str = response.xpath('//meta[@name="publicationdate"]/@content').extract_first()
        publication_date = datetime.strptime(publication_date_str, '%d/%m/%Y')
        publication_date = SAST.localize(publication_date)

        body_html = "".join(response.css("#body_content p").extract())
        body_text = remove_tags(body_html, encoding='utf-8')

        for string in SKIP_STRINGS:
            suffix = body_text[-20:]
            if unicode(string, 'utf-8') in suffix:
                self.logger.info("Skipping %s because suffix %r contains %r",
                                 canonical_url,
                                 suffix,
                                 string)
                return

        item = ScrapenewsItem()
        item['body_html'] = response.css("#body_content").extract_first()
        item['title'] = response.xpath('//meta[@name="title"]/@content').extract_first()
        item['byline'] = response.xpath('//meta[@name="author"]/@content').extract_first()
        item['published_at'] = publication_date.isoformat()
        item['retrieved_at'] = datetime.utcnow().isoformat()
        item['url'] = canonical_url
        item['file_name'] = response.url.split('/')[-1]
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item

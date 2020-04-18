# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz
from w3lib.html import remove_tags

SAST = pytz.timezone('Africa/Johannesburg')

# Note the b prefix is now needed in PY3 so that symbols translate appropriate
# correctly. When then convert from bytes to str to match the plain text items.
SKIP_STRINGS = [
    b'\xc2\xa9'.decode('utf-8'),     # copyright
    b'\xe2\x80\x91'.decode('utf-8'), # NON-BREAKING HYPHEN
    b'\xe2\x80\x92'.decode('utf-8'), # FIGURE DASH
    b'\xe2\x80\x93'.decode('utf-8'), # EN DASH
    b'\xe2\x80\x94'.decode('utf-8'), # EM DASH
    b'\xe2\x80\x95'.decode('utf-8'), # HORIZONTAL BAR
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

    sitemap_urls = ['https://mg.co.za/sitemap_index.xml']

    sitemap_rules = [
        ('mg.co.za/article', 'parse'),
    ]

    publication_name = 'Mail & Guardian'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()

        ## Skip excluded sections
        section = response.css('a.section').xpath('text()').extract_first()
        if section and section.lower() in IGNORE_SECTIONS:
            self.logger.info("Skipping %s because section is %s", canonical_url, section)
            return

        ## Skip syndicated content
        body_html = "".join(response.css("#body_content p").extract())
        body_text = remove_tags(body_html)

        for string in SKIP_STRINGS:
            suffix = body_text[-20:]
            if string in suffix:
                self.logger.info("Skipping %s because suffix %r contains %r",
                                 canonical_url,
                                 suffix,
                                 string)
                return

        publication_date_str = response.xpath('//meta[@name="publicationdate"]/@content').extract_first()
        publication_date = datetime.strptime(publication_date_str, '%d/%m/%Y')
        publication_date = SAST.localize(publication_date)


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

# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from businesslivemixin import BusinessLiveMixin

class BusinessLiveSpider(BusinessLiveMixin, SitemapSpider):
    name = 'businesslivesitemap'
    allowed_domains = ['www.businesslive.co.za']

    sitemap_urls = ['https://www.businesslive.co.za/sitemap.xml']
    sitemap_follow = ['politics', 'companies', 'people', 'national', 'news', 'special-reports', 'economy', 'markets']
    sitemap_rules = [('.*', 'parse_item')]

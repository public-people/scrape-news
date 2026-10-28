# -*- coding: utf-8 -*-

from scrapenews.spiders.timeslive import TimesliveSpider


class SundayTimesSpider(TimesliveSpider):
    """
    Sunday Times is now hosted on its own domain (sundaytimes.timeslive.co.za)
    but uses the same Arc publishing platform as TimesLIVE.
    """

    name = 'sundaytimes'
    allowed_domains = ['www.sundaytimes.timeslive.co.za']
    sitemap_urls = ['https://www.sundaytimes.timeslive.co.za/arc/outboundfeeds/sitemap-news-index/']

    sitemap_rules = [
        (r'/news/', 'parse'),
        (r'/business/', 'parse'),
        (r'/investigations/', 'parse'),
        (r'/opinion/', 'parse'),
    ]

    publication_name = 'Sunday Times'

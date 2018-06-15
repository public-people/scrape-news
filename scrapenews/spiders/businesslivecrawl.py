# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from businesslivemixin import BusinessLiveMixin

class BusinessLiveCrawlSpider(BusinessLiveMixin, CrawlSpider):
    name = 'businesslivecrawl'
    allowed_domains = ['www.businesslive.co.za']
    start_urls = ['http://www.businesslive.co.za/']

    rules = (
        # Extract links containing a date in the url and parse them with the spider's method parse_item
        Rule(LinkExtractor(
            allow=(r'\d{4}-\d{2}-\d{2}',),
            deny=(r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',),
        ), callback='parse_item'),

        # Extract links matching these categories and follow links from them
        Rule(LinkExtractor(
            allow=(r'fm|bd|rdm|bt|ft',),
            deny=(r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',)
        ), follow=True),
    )

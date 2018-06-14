# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime

class DailyvoiceSpider(CrawlSpider):
    name = 'dailyvoice'
    allowed_domains = ['dailyvoice.co.za']

    start_urls = ['https://www.dailyvoice.co.za']

    link_extractor = LinkExtractor(
        allow=('https://www.dailyvoice.co.za', ),
        # being ultra specific for the 'allow' because 'dailyvoice.co.za' was
        # in some of the external links eg instagram
        deny=(
            'dailyvoice.co.za/about-us',
            'dailyvoice.co.za/cdn-cgi/l/email-protection',
            'dailyvoice.co.za/competitions',
            'dailyvoice.co.za/contact-us',
            'dailyvoice.co.za/feedback',
            'dailyvoice.co.za/lifestyle-',
            'dailyvoice.co.za/multimedia',
            'dailyvoice.co.za/opinion',
            'dailyvoice.co.za/privacy-policy',
            'dailyvoice.co.za/sport',
            'dailyvoice.co.za/terms-and-conditions',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Daily Voice'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            body_html = response.css('div.articleBodyMore').extract_first()
            byline = response.xpath('//strong[@itemprop="name"]/text()').extract_first()
            publication_date = response.xpath('//span[@itemprop="datePublished"]/@content').extract_first()
            # u'2018-06-12T13:48:00.000Z'

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title
                item['byline'] = byline
                item['published_at'] = publication_date
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/')[-1]
                item['publication_name'] = self.publication_name
                item['spider_name'] = self.name

                yield item
            else:
                self.logger.info("No body found for %s", response.url)
                # should we be using canonical_url instead of response.url for the above?

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/news/' not in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/news/international/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

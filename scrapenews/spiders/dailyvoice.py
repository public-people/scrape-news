# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DailyvoiceSpider(CrawlSpider):
    name = 'dailyvoice'
    allowed_domains = ['dailyvoice.co.za']

    start_urls = ['https://www.dailyvoice.co.za']

    link_extractor = LinkExtractor(
        allow=(r'/.*\d{4}-\d{2}-\d{2}.*', ),
        deny=(
            r'/#',
            r'/about-us',
            r'/cdn-cgi/',
            r'/competitions',
            r'/contact-us',
            r'/feedback',
            r'/lifestyle-',
            r'/multimedia',
            r'/opinion',
            r'/privacy-policy',
            r'/sport',
            r'/terms-and-conditions',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Daily Voice'

    def parse_item(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url
        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        article_body = response.css('[class*=article_]')
        if not article_body:
            article_body = response.css('article')
        if not article_body:
            self.logger.info("No body found for %s", response.url)
            return

        body_html = article_body.get()

        byline = response.css('.b-author-bio__author-name::text').get()
        if not byline:
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
        item['publication_name'] = self.publication_name
        item['spider_name'] = self.name

        yield item

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/news/' not in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

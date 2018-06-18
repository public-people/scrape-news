# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')

class dfaSpider(CrawlSpider):
    name = 'dfa'
    allowed_domains = ['dfa.co.za']

    start_urls = ['https://www.dfa.co.za']

    link_extractor = LinkExtractor(
        allow=('https://www.dfa.co.za', ),
        deny=(
            '/?filter_by',
            'dfa.co.za/about-us',
            'dfa.co.za/author',
            'dfa.co.za/cdn-cgi/l/email-protection',
            'dfa.co.za/international-',
            'dfa.co.za/lifestyle-',
            'dfa.co.za/matric-2017',
            'dfa.co.za/opinion-',
            'dfa.co.za/privacy-policy',
            'dfa.co.za/sport',
            'dfa.co.za/uncategorized',
            '//pinterest.com/',
            '//plus.google.com/',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Diamond Fields Advertiser'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            article_body = response.css('div.td-post-content')
            body_html = " ".join(article_body.xpath('//p').extract())
            byline = response.css('div.td-post-author-name').css('::text').extract()[2]

            publication_date_str = response.xpath('//time/@datetime').extract_first()
            # u'2018-06-14T11:00:00+00:00'
            publication_date = datetime.strptime(publication_date_str[0:19], '%Y-%m-%dT%H:%M:%S')
            # datetime.datetime(2018, 6, 14, 11, 0)
            publication_date = SAST.localize(publication_date)
            # datetime.datetime(2018, 6, 14, 11, 0, tzinfo=<DstTzInfo 'Africa/Johannesburg' SAST+2:00:00 STD>)

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title
                item['byline'] = byline
                item['published_at'] = publication_date.isoformat()
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/')[-2]
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

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
                if '/south-african-news/' not in link.url:
                    self.logger.info("Ignoring %s", link.url)
                    continue
                else:
                    yield link
            else:
                yield link

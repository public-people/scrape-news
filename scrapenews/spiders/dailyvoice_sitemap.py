# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DailyVoiceSpider(SitemapSpider):
    name = 'dailyvoice'
    allowed_domains = ['www.dailyvoice.co.za']

    sitemap_urls = [
        # 'https://www.dailyvoice.co.za/robots.txt',
        # 'https://www.dailyvoice.co.za/sitemap.xml',
        'https://www.dailyvoice.co.za/sitemap-1.xml',
    ]
    # sitemap_rules = [
    #     ('/news/western-cape', 'parse'),
    #     ('/news/national', 'parse'),
    #     ('/news/politics', 'parse'),
    # ]
    # sitemap_follow = [
    #     'www.dailyvoice.co.za/news/western-cape',
    #     'www.dailyvoice.co.za/news/national',
    #     'www.dailyvoice.co.za/news/politics',
    # ]

    publication_name = 'Daily Voice'

    def parse(self, response):
        if '/news/' not in response.url:
            self.logger.info("Ignoring %s", response.url)
            return

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('div.articleBodyMore')

        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//strong[@itemprop="name"]/text()').extract_first()
            publication_date_str = response.xpath('//span[@itemprop="datePublished"]/text()').extract_first()
            # '24 May 2018, 1:33pm'
            publication_date = datetime.strptime(publication_date_str, '%d %B %Y, %I:%M%p')
            # datetime.datetime(2018, 5, 24, 13, 33)
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = canonical_url
            item['file_name'] = response.url.split('/')[-1]
            item['spider_name'] = self.name
            item['publication_name'] = self.publication_name

            yield item

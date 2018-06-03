# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class DiamondSpider(SitemapSpider):
    name = 'diamondfieldsadvertiser'
    allowed_domains = ['www.dfa.co.za']

    sitemap_urls = ['https://www.dfa.co.za/robots.txt']
    sitemap_follow = [
        'www.dfa.co.za/news',
        'www.dfa.co.za/south-african-news',
    ]

    publication_name = 'Diamond Fields Advertiser'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('div.td-post-content')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.css('div.td-post-author-name').css('::text').extract()[2]
            publication_date_str = response.css('time.entry-date').xpath('text()').extract_first()
            # 'June 1, 2018'
            publication_date = datetime.strptime(publication_date_str, '%B %d, %Y')
            # datetime.datetime(2018, 6, 1, 0, 0)
            publication_date = SAST.localize(publication_date)

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

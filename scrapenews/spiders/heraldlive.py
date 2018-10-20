# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class HeraldLiveSpider(SitemapSpider):
    name = 'hearaldlive'
    allowed_domains = ['www.heraldlive.co.za']

    sitemap_urls = ['www.heraldlive.co.za/robots.txt']
    sitemap_follow = [
        '^https://www.heraldlive.co.za/news/((?!eish).)*$'
    ]

    publication_name = 'Herald Live'

    def parse(self, response):
        title = response.xpath('//head/title/text()').extract_first()
        self.logger.info('{} {}'.format(response.url, title))
        article_body = response.xpath('//div[@itemprop="articleBody"]')
        if article_body:
            body_html = article_body.extract_first().strip()
            byline_temp = response.css('.article-author').xpath('text()').extract_first().strip()
            byline = byline_temp[:-2] if byline_temp[-2:] == " -" else byline_temp
            publication_date_str = response.css('.article-pub-date').xpath('text()').extract_first().strip()

            try:
                publication_date = datetime.strptime(publication_date_str, '%-d %B %Y')
            except ValueError:
                if
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-1]
            item['spider_name'] = self.name

            item['publication_name'] = self.publication_name

            yield item

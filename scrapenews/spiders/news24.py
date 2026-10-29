# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class News24Spider(SitemapSpider):
    name = 'news24'
    allowed_domains = ['www.news24.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    sitemap_urls = ['https://www.news24.com/news24/sitemapindex/0/2026/10/28']
    sitemap_rules = [
        (r'/southafrica/', 'parse'),
        (r'/world/', 'parse'),
        (r'/africa/', 'parse'),
        (r'/business/', 'parse'),
        (r'/politics/', 'parse'),
        (r'/columnists/', 'parse'),
        (r'/green/', 'parse'),
        (r'/obituaries/', 'parse'),
        (r'/pressreleases/', 'parse'),
    ]

    publication_name = 'News24'

    def parse(self, response):
        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('.article')
        if article_body:
            body_html = article_body.get()
            byline = response.css('meta[name=author]::attr(content)').get()
            publication_date_str = response.css('meta[name=publisheddate]::attr(content)').get()

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
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-1]
            item['spider_name'] = self.name
            item['publication_name'] = self.publication_name

            yield item
        self.logger.info("")

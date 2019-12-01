import pytz
from datetime import datetime

from scrapenews import lib
from scrapenews.items import ScrapenewsItem
from .sitemap import SitemapSpider

SAST = pytz.timezone('Africa/Johannesburg')


class IOLSpider(SitemapSpider):
    name = 'iol'
    allowed_domains = ['www.iol.co.za']

    sitemap_urls = ['https://www.iol.co.za/robots.txt']
    sitemap_follow = [
        '^https://www.iol.co.za/news/((?!eish).)*$',
        'www.iol.co.za/business-report',
        'www.iol.co.za/politics',
        'www.iol.co.za/personal-finance',
    ]

    publication_name = 'IOL News'

    def parse(self, response):

        title = response.xpath('//header/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//div[@itemprop="articleBody"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//span[@itemprop="author"]/strong/text()').extract_first()
            publication_date_str = response.xpath('//span[@itemprop="datePublished"]/@content').extract_first()

            publication_date = lib.parse_date_hour_min(publication_date_str)
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

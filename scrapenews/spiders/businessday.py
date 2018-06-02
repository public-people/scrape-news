# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class BusinessDaySpider(SitemapSpider):
    name = 'businessday'
    allowed_domains = ['www.businesslive.co.za']

    sitemap_urls = ['https://www.businesslive.co.za/sitemap.xml']
    sitemap_follow = ['politics', 'companies', 'people', 'national', 'news', 'special-reports']

    publication_name = 'Business Day'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        if canonical_url:
            url = canonical_url
        else:
            url = response.url

        title = response.xpath('//h1[@class="article-title article-title-primary"]/span/text()').extract_first()
        self.logger.info('%s %s', url, title)
        article_body = response.xpath('//div[@class="article-content  article-style-None"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//span[@id="authors"]/text()').extract_first()
            publication_date_str = response.xpath('//div[@class="article-pub-date "]/text()').extract_first()
            publication_date_str = publication_date_str.strip()
            publication_date = datetime.strptime(publication_date_str, '%d %B %Y - %H:%M')
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = url
            item['file_name'] = url.split('/')[-2]
            item['spider_name'] = self.name

            item['publication_name'] = self.publication_name

            yield item

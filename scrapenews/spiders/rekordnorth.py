# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class RekordNorthSpider(CrawlSpider):
    name = 'rekordnorth'
    allowed_domains = ['citizen.co.za']
    start_urls = ['https://www.citizen.co.za/rekord/']

    article_link_extractor = LinkExtractor(
        allow=(r'/rekord/.*\d{4}/\d{2}/\d{2}/', ),
        deny=(r'/attachment/',),
        allow_domains=['citizen.co.za']
    )
    category_link_extractor = LinkExtractor(
        allow=(r'/rekord/category/', ),
        allow_domains=['citizen.co.za'],
        deny=r'opinion-edition|lifestyle-news'
    )

    rules = (
        Rule(article_link_extractor, callback='parse_item', follow=True),
        Rule(category_link_extractor, follow=True),
    )

    publication_name = 'Rekord Pretoria-North'

    def parse_item(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url
        title = response.css('h1::text').get()
        og_type = response.css('meta[property="og:type"]::attr(content)').get()
        if og_type == 'article':
            article_body = response.css('.post-content')
            body_html = article_body.get()
            byline = response.css('div.author-name').css('::text').get()

            publication_date_str = response.css('time::attr(datetime)').get()
            if publication_date_str:
                publication_date = datetime.fromisoformat(publication_date_str[:19])
                publication_date = SAST.localize(publication_date)
            else:
                publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title.strip() if title else ''
                item['byline'] = byline.strip() if byline else ''
                item['published_at'] = publication_date.isoformat()
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/')[-2]
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

                yield item
            else:
                self.logger.info("No body found for %s", canonical_url)

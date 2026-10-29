# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class groundupSpider(CrawlSpider):
    name = 'groundup'
    allowed_domains = ['groundup.org.za']

    start_urls = ['https://www.groundup.org.za/']

    link_extractor = LinkExtractor(
        allow=(r'/article/', ),
        deny=(
            r'https://www\.facebook\.com/',
            r'https://twitter\.com/',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'GroundUp'

    def parse_item(self, response):
        og_url = response.css('meta[property="og:url"]::attr(content)').get()
        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        og_type = response.css('meta[property="og:type"]::attr(content)').get()

        if og_type == 'article':
            subtitle = response.xpath('//p[@id="article_subtitle"]').css('::text').get()
            photo_caption = response.xpath('//figcaption[@id="article_primary_image_caption"]/text()').get()
            article_body = " ".join(response.xpath('//div[@id="article_body"]').css('::text').extract())
            if subtitle and photo_caption:
                body_html = subtitle + photo_caption + article_body
            elif subtitle and not photo_caption:
                body_html = subtitle + article_body
            elif photo_caption and not subtitle:
                body_html = photo_caption + article_body
            else:
                body_html = article_body
            byline = response.xpath('//a[@rel="author"]/text()').get()
            publication_date_str = response.xpath('//time/@datetime').get()
            if publication_date_str:
                publication_date = datetime.strptime(publication_date_str[:10], '%Y-%m-%d')
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
                item['url'] = og_url or response.url
                item['file_name'] = response.url.split('/')[-2]
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

                yield item
            else:
                self.logger.info("No body found for %s", response.url)

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

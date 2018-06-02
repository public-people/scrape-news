# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class TimesliveSpider(SitemapSpider):
    name = 'timeslive'
    allowed_domains = ['www.timeslive.co.za']

    sitemap_urls = ['https://www.timeslive.co.za/robots.txt']
    sitemap_follow = [
        'www.timeslive.co.za/sitemap/anc-conference-2017/',
        'www.timeslive.co.za/sitemap/news/',
        'www.timeslive.co.za/sitemap/politics/',
        'www.timeslive.co.za/sitemap/investigations/',
        'www.timeslive.co.za/sitemap/opinion-and-analysis/',
        'www.timeslive.co.za/sitemap/business/',
    ]

    publication_name = 'Times Live'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()

        title = response.xpath('//h1/span/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('div.article-widget-text')
        if article_body:
            # join multiple text sections
            body_html = " ".join(article_body.extract())
            byline_includes_by = response.xpath('//span[@class="heading-author"]/text()').extract()
            byline_str = " ".join(byline_includes_by)
            byline_no_by = (byline_str).split(" ")[1:]
            byline = " ".join(byline_no_by)

            publication_date_str = response.css('div.article-pub-date').xpath('text()').extract()[0].strip()
            # '03 May 2018 - 19:17'
            publication_date = datetime.strptime(publication_date_str, '%d %B %Y - %H:%M')
            # datetime.datetime(2018, 5, 3, 19, 17)

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

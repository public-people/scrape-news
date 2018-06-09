# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class BusinessLiveSpider(SitemapSpider):
    name = 'businesslive'
    allowed_domains = ['www.businesslive.co.za']

    sitemap_urls = ['https://www.businesslive.co.za/sitemap.xml']
    sitemap_follow = ['politics', 'companies', 'people', 'national', 'news', 'special-reports', 'economy', 'markets']

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        if canonical_url:
            url = canonical_url
        else:
            url = response.url

        title = response.css('h1.article-title-primary').xpath('span/text()').extract_first()
        self.logger.info('%s %s', url, title)

        # Ignore premium content articles
        is_premium_content = response.css('div.premium-alert').xpath("h3/text()").extract_first() == 'This article is reserved for our subscribers.'
        if is_premium_content:
            self.logger.info("Ignoring %s", url)
            return

        article_body = response.css('div.article-widget-text')
        if article_body:
            # join multiple text sections
            body_html = " ".join(article_body.extract())
            byline = response.css('span.heading-author').xpath('text()').extract_first()
            publication_date_str = response.css('div.article-pub-date').xpath('text()').extract_first().strip()
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

            publication_urls = {
                'bd': 'Business Day',
                'fm': 'Financial Mail',
                'rdm': 'Rand Daily Mail',
                'bt': 'Business Times',
                'ft': 'Financial Times'
            }
        
            url_part = url.split('/')[3]

            item['publication_name'] = publication_urls.get(url_part, 'Business Day')

            yield item

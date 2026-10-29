# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz
import json

SAST = pytz.timezone('Africa/Johannesburg')


class ewnSpider(CrawlSpider):
    name = 'ewn'
    allowed_domains = ['ewn.co.za']

    start_urls = ['https://ewn.co.za']

    link_extractor = LinkExtractor(
        allow=(r'/\d{4}/\d{2}/\d{2}/',),
        deny=()
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Eyewitness News'

    def parse_item(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url
        title = response.css('h1::text').get()
        self.logger.info('%s %s', response.url, title)

        # Try to find article body - ewn uses dynamic Vue/Tailwind classes
        article_body = response.css('article.richtext')
        if not article_body:
            article_body = response.css('article')
        if not article_body:
            self.logger.info("No body found for %s", response.url)
            return

        body_html = article_body.get()

        byline = response.css('meta[name=author]::attr(content)').get()

        publication_date = None
        # Try JSON-LD for date
        for script in response.css('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.css('::text').get(''))
                if data.get('@type') == 'NewsArticle':
                    date_str = data.get('datePublished')
                    if date_str:
                        publication_date = datetime.fromisoformat(date_str)
                        publication_date = publication_date.astimezone(SAST)
                    author_data = data.get('author')
                    if author_data and not byline:
                        if isinstance(author_data, dict):
                            byline = author_data.get('name', '')
                        elif isinstance(author_data, list) and author_data:
                            byline = author_data[0].get('name', '')
                    break
            except (json.JSONDecodeError, ValueError):
                continue

        if not publication_date:
            publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

        item = ScrapenewsItem()
        item['body_html'] = body_html
        item['title'] = title.strip() if title else ''
        item['byline'] = byline.strip() if byline else ''
        item['published_at'] = publication_date.isoformat()
        item['retrieved_at'] = datetime.utcnow().isoformat()
        item['url'] = canonical_url
        item['file_name'] = response.url.split('/').pop()
        item['spider_name'] = self.name
        item['publication_name'] = self.publication_name

        yield item

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            yield link

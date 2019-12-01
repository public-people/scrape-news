import pytz
from datetime import datetime

from scrapenews import lib
from scrapenews.items import ScrapenewsItem
from .sitemap import SitemapSpider


SAST = pytz.timezone('Africa/Johannesburg')


class DailMaverickSpider(SitemapSpider):
    name = 'dailymaverick'
    allowed_domains = ['www.dailymaverick.co.za']

    sitemap_urls = ['https://www.dailymaverick.co.za/sitemap_index.xml']
    sitemap_follow = ['article-sitemap']

    publication_name = 'Daily Maverick'

    def parse(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        if canonical_url:
            url = canonical_url
        else:
            url = response.url

        if '/opinionistas' in url:
            self.logger.info("Ignoring %s", url)
            return

        title = response.xpath('//div[@class="titles"]/h1/text()').extract_first()
        self.logger.info('%s %s', url, title)
        article_body = response.xpath('//div[@class="article-container"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//meta[@name="author"]/@content').extract_first()
            publication_date_str = response.xpath('//meta[@name="published"]/@content').extract_first()

            publication_date = lib.parse_date(publication_date_str)
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

import pytz
from datetime import datetime

from scrapenews.items import ScrapenewsItem
from scrapenews import lib
from .sitemap import SitemapSpider


SAST = pytz.timezone('Africa/Johannesburg')


class News24Spider(SitemapSpider):
    name = 'news24'
    allowed_domains = ['www.news24.com']

    sitemap_urls = ['https://www.news24.com/robots.txt']
    sitemap_rules = [
        ('www.news24.com/SouthAfrica/News', 'parse'),
        ('www.news24.com/Columnists', 'parse'),
        ('www.news24.com/Green/News', 'parse'),
        ('www.news24.com/Obituaries', 'parse'),
        ('www.news24.com/PressReleases', 'parse'),
    ]

    publication_name = 'News24'

    def parse(self, response):
        if '/News/' not in response.url:
            self.logger.info("Ignoring %s", response.url)
            return

        title = response.xpath('//div[contains(@class, "article_details")]/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.xpath('//article[@id="article-body"]')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//div[contains(@class, "ByLineWidth")]/p/text()').extract_first()
            publication_date_str = response.xpath('//span[@id="spnDate"]/text()').extract_first()
            accreditation = response.xpath(
                '//div[contains(@class, "ByLineWidth")]/div[contains(@class, "accreditation")]/a/@href'
            ).extract_first()

            publication_date = lib.parse_date(publication_date_str)
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
            if accreditation:
                item['publication_name'] += " with " + accreditation[1:]

            yield item

        self.logger.info("")

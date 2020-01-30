import pytz
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews.items import ScrapenewsItem
from scrapenews import lib


SAST = pytz.timezone('Africa/Johannesburg')


class groundupSpider(CrawlSpider):
    name = 'groundup'
    allowed_domains = ['groundup.org.za']

    start_urls = ['https://www.groundup.org.za/']

    link_extractor = LinkExtractor(
        allow=('https://www.groundup.org.za/article/', ),
        deny=(
            'https://www.facebook.com/',
            'https://twitter.com/',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'GroundUp'

    def parse_item(self, response):

        og_url = response.xpath('//meta[@property="og:url"]/@content').extract_first()
        # no 'canonical' that I could find
        title = response.xpath('//h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using og_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()

        if og_type == 'article':
            subtitle = response.xpath('//p[@id="article_subtitle"]').css('::text').extract_first()
            photo_caption = response.xpath('//figcaption[@id="article_primary_image_caption"]/text()')\
                .extract_first()
            article_body = " ".join(response.xpath('//div[@id="article_body"]').css('::text').extract())

            if subtitle and photo_caption:
                body_html = subtitle + photo_caption + article_body
            elif subtitle and not photo_caption:
                body_html = subtitle + article_body
            elif photo_caption and not subtitle:
                body_html = photo_caption + article_body
            else:
                body_html = article_body

            byline = response.xpath('//a[@rel="author"]/text()').extract_first()
            publication_date_str = response.xpath('//time/@datetime').extract_first()
            publication_date = lib.parse_ISO8601_date(publication_date_str)
            publication_date = SAST.localize(publication_date)

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title
                item['byline'] = byline
                item['published_at'] = publication_date.isoformat()
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = og_url
                item['file_name'] = response.url.split('/')[-2]
                # should we be using og_url instead of response.url for the above?
                item['spider_name'] = self.name
                item['publication_name'] = self.publication_name

                yield item

            else:
                self.logger.info("No body found for %s", response.url)
                # should we be using og_url instead of response.url for the above?

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

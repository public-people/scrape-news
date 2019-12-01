import pytz
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews.items import ScrapenewsItem
from scrapenews import lib


SAST = pytz.timezone('Africa/Johannesburg')

IGNORE_URLS = {
    'https://www.dailyvoice.co.za/news/business',
    'https://www.dailyvoice.co.za/news/international',
    'https://www.dailyvoice.co.za/news/national',
    'https://www.dailyvoice.co.za/news/politics',
    'https://www.dailyvoice.co.za/news/western-cape',
}


class DailyvoiceSpider(CrawlSpider):
    name = 'dailyvoice'
    allowed_domains = ['dailyvoice.co.za']

    start_urls = ['https://www.dailyvoice.co.za']

    link_extractor = LinkExtractor(
        allow=('https://www.dailyvoice.co.za', ),
        deny=(
            'dailyvoice.co.za#',
            'dailyvoice.co.za/about-us',
            'dailyvoice.co.za/cdn-cgi/l/email-protection',
            'dailyvoice.co.za/competitions',
            'dailyvoice.co.za/contact-us',
            'dailyvoice.co.za/feedback',
            'dailyvoice.co.za/lifestyle-',
            'dailyvoice.co.za/multimedia',
            'dailyvoice.co.za/opinion',
            'dailyvoice.co.za/privacy-policy',
            'dailyvoice.co.za/sport',
            'dailyvoice.co.za/terms-and-conditions',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Daily Voice'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            article_body = response.css('div.article-body')
            body_html = " ".join(article_body.xpath('//p').css('::text').extract())
            byline = response.xpath('//strong[@itemprop="name"]/text()').extract_first()
            publication_date_str = response.xpath('//meta[@itemprop="datePublished"]/@content').extract_first()

            # Date format changes, previously it was:
            #   '18 June 2018, 09:01am'
            #   '%d %B %Y, %I:%M%p'
            publication_date = lib.parse_date_hour_min_sec(publication_date_str)
            publication_date = SAST.localize(publication_date)
            published_at = publication_date.isoformat()

            if body_html:
                item = ScrapenewsItem()
                item['body_html'] = body_html
                item['title'] = title
                item['byline'] = byline
                item['published_at'] = published_at
                item['retrieved_at'] = datetime.utcnow().isoformat()
                item['url'] = canonical_url
                item['file_name'] = response.url.split('/')[-1]
                item['publication_name'] = self.publication_name
                item['spider_name'] = self.name

                yield item
            else:
                self.logger.info("No body found for %s", response.url)
                # should we be using canonical_url instead of response.url for the above?

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/news/' not in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/news/international/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif link.url in IGNORE_URLS:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

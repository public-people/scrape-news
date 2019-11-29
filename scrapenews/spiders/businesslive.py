from __future__ import absolute_import
import pytz
from datetime import datetime

from scrapy.spiders import SitemapSpider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapenews.items import ScrapenewsItem


SAST = pytz.timezone('Africa/Johannesburg')


class BusinessLiveMixin():

    def parse_item(self, response):
        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        if canonical_url:
            url = canonical_url
        else:
            url = response.url

        title = response.css('h1.article-title-primary').xpath('span/text()').extract_first()
        self.logger.info('%s %s', url, title)

        # Ignore premium content articles
        is_premium_content = response.css('div.premium-alert').xpath("h3/text()")\
            .extract_first() == 'This article is reserved for our subscribers.'
        if is_premium_content:
            self.logger.info("Ignoring premium content %s", url)
            return

        article_body = response.css('div.article-widget-text')
        if article_body:
            # join multiple text sections
            body_html = " ".join(article_body.extract())
            byline = response.css('span.heading-author').xpath('text()').extract_first()
            publication_date_str = response.css('div.article-pub-date')\
                .xpath('text()').extract_first().strip()
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
        else:
            self.logger.info("No body found for %s", response.url)


class BusinessLiveSpider(BusinessLiveMixin, SitemapSpider):
    name = 'businesslivesitemap'
    allowed_domains = ['www.businesslive.co.za']

    sitemap_urls = ['https://www.businesslive.co.za/sitemap.xml']
    sitemap_follow = ['politics', 'companies', 'people', 'national', 'news',
                      'special-reports', 'economy', 'markets']
    sitemap_rules = [('.*', 'parse_item')]


class BusinessLiveCrawlSpider(BusinessLiveMixin, CrawlSpider):
    name = 'businesslivecrawl'
    allowed_domains = ['www.businesslive.co.za']
    start_urls = ['http://www.businesslive.co.za/']

    rules = (
        # Extract links containing a date in the url and parse them with the spider's method parse_item
        Rule(LinkExtractor(
            allow=(r'\d{4}-\d{2}-\d{2}',),
            deny=(
                r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',
            ),
        ), callback='parse_item'),

        # Extract links matching these categories and follow links from them
        Rule(LinkExtractor(
            allow=(r'fm|bd|rdm|bt|ft',),
            deny=(
                r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',
            )
        ), follow=True),
    )

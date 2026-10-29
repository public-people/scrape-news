from scrapy.spiders import SitemapSpider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


def parse_arc_article(response, spider, publication_name):
    canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url
    title = response.css('h1::text').get()
    spider.logger.info('%s %s', response.url, title)

    article_body = response.css('.b-article-body')
    if not article_body:
        article_body = response.css('article')
    if not article_body:
        spider.logger.info("No body found for %s", response.url)
        return

    body_html = article_body.get()

    byline = response.css('.b-author-bio__author-name::text').get()
    if not byline:
        byline = response.css('meta[name=author]::attr(content)').get()

    publication_date_str = response.css('time[datetime]::attr(datetime)').get()
    if publication_date_str:
        publication_date = datetime.fromisoformat(publication_date_str)
        publication_date = publication_date.astimezone(SAST)
    else:
        publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

    item = ScrapenewsItem()
    item['body_html'] = body_html
    item['title'] = title.strip() if title else ''
    item['byline'] = byline.strip() if byline else ''
    item['published_at'] = publication_date.isoformat()
    item['retrieved_at'] = datetime.utcnow().isoformat()
    item['url'] = canonical_url
    item['file_name'] = response.url.split('/')[-2]
    item['spider_name'] = spider.name
    item['publication_name'] = publication_name
    yield item


class BusinessLiveMixin():

    def parse_item(self, response):
        canonical_url = response.css('link[rel=canonical]::attr(href)').get() or response.url
        url = canonical_url

        title = response.css('h1::text').get()
        self.logger.info('%s %s', url, title)

        # Ignore premium content articles
        is_premium_content = response.css('div.premium-alert').xpath("h3/text()").get() == 'This article is reserved for our subscribers.'
        if is_premium_content:
            self.logger.info("Ignoring premium content %s", url)
            return

        article_body = response.css('.b-article-body')
        if not article_body:
            article_body = response.css('article')
        if article_body:
            body_html = article_body.get()
            byline = response.css('.b-author-bio__author-name::text').get()
            if not byline:
                byline = response.css('meta[name=author]::attr(content)').get()

            publication_date_str = response.css('time[datetime]::attr(datetime)').get()
            if publication_date_str:
                publication_date = datetime.fromisoformat(publication_date_str)
                publication_date = publication_date.astimezone(SAST)
            else:
                publication_date = datetime.utcnow().replace(tzinfo=pytz.UTC)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title.strip() if title else ''
            item['byline'] = byline.strip() if byline else ''
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
    allowed_domains = ['www.businessday.co.za']

    sitemap_urls = ['https://www.businessday.co.za/arc/outboundfeeds/sitemap-news-index/']
    sitemap_rules = [
        (r'/news/', 'parse_item'),
        (r'/politics/', 'parse_item'),
        (r'/economy/', 'parse_item'),
        (r'/companies/', 'parse_item'),
        (r'/markets/', 'parse_item'),
    ]


class BusinessLiveCrawlSpider(BusinessLiveMixin, CrawlSpider):
    name = 'businesslivecrawl'
    allowed_domains = ['www.businessday.co.za']
    start_urls = ['https://www.businessday.co.za/']

    rules = (
        Rule(LinkExtractor(
            allow=(r'\d{4}-\d{2}-\d{2}',),
            deny=(r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',),
        ), callback='parse_item'),

        Rule(LinkExtractor(
            allow=(r'fm|bd|rdm|bt|ft',),
            deny=(r'/(opinion|world|sport|life|multimedia|redzone|technology|popcorn|lifestyle|wsj|sign-up|careers)/',)
        ), follow=True),
    )

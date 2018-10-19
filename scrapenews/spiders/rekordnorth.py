# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')

class dfaSpider(CrawlSpider):
    name = 'rekordnorth'
    allowed_domains = ['rekordnorth.co.za']
    start_urls = ['https://rekordnorth.co.za/category/news-headlines/local-news/']

    link_extractor = LinkExtractor(
        allow=('https://rekordnorth.co.za', ),
        deny=(
            'rekordnorth.co.za/pretoria-north-news-team',
            'rekordnorth.co.za/epapers',
            'rekordnorth.co.za/feat/title-deeds/',
            'rekordnorth.co.za/advertise-online/',
            'rekordnorth.co.za/category/featured-content/',
            'rekordnorth.co.za/beauty-health-all-year-round/',
            'rekordnorth.co.za/rss-output/',
            'rekordnorth.co.za/all4women',
            'rekordnorth.co.za/national-news/',
            'rekordnorth.co.za/local-motoring-news/',
            'rekordnorth.co.za/category/image-gallery/',
            'rekordnorth.co.za/category/image-gallery/general-news/',
            'rekordnorth.co.za/category/image-gallery/community/',
            'rekordnorth.co.za/category/image-gallery/sport-news/',
            'rekordnorth.co.za/category/image-gallery/school-news/',
            'rekordnorth.co.za/video-gallery/',
            'rekordnorth.co.za/category/opinion-edition/letters/',
            'rekordnorth.co.za/category/opinion-edition/blogs/',
            'rekordnorth.co.za/category/opinion-edition/blogs/simply-delicious/',
            'rekordnorth.co.za/category/lifestyle-news/competitions-in-pretoria-north/',
            'rekordnorth.co.za/category/lifestyle-news/entertainment-news/',
            'rekordnorth.co.za/events/event/',
            'rekordnorth.co.za/category/news-headlines/',
            'rekordnorth.co.za/category/sports-news/',
            'rekordnorth.co.za/category/opinion-edition/',
            'rekordnorth.co.za/category/lifestyle-news/',
            'rekordnorth.co.za/online-classifieds/',
            'rekordnorth.co.za/place-ad/',
            'rekordnorth.co.za/terms-and-conditions/',
            'rekordnorth.co.za/privacy-policy/',
            'rekordnorth.co.za/builders/',
            'rekordnorth.co.za/property/for-sale/',
            'rekordnorth.co.za/property/to-rent/',
            'rekordnorth.co.za/rest-assured/',
            'rekordeast.co.za/parenting/',
            'rekordnorth.co.za/support-local-business/',
            'rekordnorth.co.za/i-love-my-city/',
            'rekordnorth.co.za/?p=128157',
            'rekordnorth.co.za/student-living/',
            'rekordnorth.co.za/be-your-best/',
            'rekordnorth.co.za/magalieskruin-centre/',
            'rekordnorth.co.za/about-us',
            '//biz.rekordnorth.co.za/',
            '//www.guzzle.co.za/',
            '//www.autodealer.co.za/',
            '//iab.com/',
            '//www.bestofpretoria.co.za/',
            '//localnewsnetwork.co.za/',
            '//www.caxton.co.za/',
            '//facebook.com/',
            '//twitter.com/',
            '//southcoastherald.co.za/',
            '//rekordcenturion.co.za/',
            '//kemptonexpress.co.za/',
            '//northglennews.co.za/',
            '//albertonrecord.co.za/',
            '//ladysmithgazette.co.za/',
            '//witbanknews.co.za/',
            '//roodepoortrecord.co.za/',
            '//southerncourier.co.za/',
            '//krugersdorpnews.co.za/',
        )
    )

    rules = (
        Rule(link_extractor, process_links='filter_links', callback='parse_item', follow=True),
    )

    publication_name = 'Rekord Pretoria-North'

    def parse_item(self, response):

        canonical_url = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        # should we be using canonical_url instead of response.url for the above?
        og_type = response.xpath('//meta[@property="og:type"]/@content').extract_first()
        if og_type == 'article':
            article_body = response.css('div.entry-content')
            body_html = " ".join(article_body.xpath('//p').extract())
            byline = response.css('div.author-name').css('::text').extract()

            publication_date_str = response.xpath('//time/@datetime').extract_first()
            # u'2018-06-14T11:00:00+00:00'
            publication_date = datetime.strptime(publication_date_str[0:19], '%Y-%m-%dT%H:%M:%S')
            # datetime.datetime(2018, 6, 14, 11, 0)
            publication_date = SAST.localize(publication_date)
            # datetime.datetime(2018, 6, 14, 11, 0, tzinfo=<DstTzInfo 'Africa/Johannesburg' SAST+2:00:00 STD>)

            if body_html:
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
            else:
                self.logger.info("No body found for %s", response.url)
                # should we be using canonical_url instead of response.url for the above?

    def filter_links(self, links):
        for link in links:
            if '?' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            if '/afp/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/international-news/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif 'cdn-cgi/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            elif '/community-toolbox/' in link.url:
                self.logger.info("Ignoring %s", link.url)
                continue
            else:
                yield link

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
        'www.timeslive.co.za/anc-conference-2017',
        'www.timeslive.co.za/news',
        'www.timeslive.co.za/politics',
        'www.timeslive.co.za/investigations',
        'www.timeslive.co.za/opinion-and-analysis',
        'www.timeslive.co.za/business',
    ]

    publication_name = 'Times Live'

    def parse(self, response):
        
        title = response.xpath('//h1/span/text()').extract_first()
        self.logger.info('%s %s', response.url, title) # check what this does
        article_body = response.xpath('//div[@class="article-widget article-widget-text"]')
        if article_body:
            body_html = article_body.extract_first()
            body_text = "\n\n".join(response.xpath('//div[@class="article-widget article-widget-text"]/div/div/p/text()').extract()) # currently unused but depending on ultimate use of body_html might this be better?
            
            byline_includes_by = response.xpath('//span[@class="heading-author"]/text()').extract()
            byline_str = " ".join(byline_includes_by)
            byline_no_by = (byline_str).split(" ")[1:]
            byline = " ".join(byline_no_by)
            
            pubdate_long = response.xpath('//div[@class="article-pub-date "]/text()').extract()[0].strip()
            day = pubdate_long.split(" ")[0]
            month = pubdate_long.split(" ")[1]
            if month == 'January':
                month = '01'
            if month == 'February':
                month = '02'
            if month == 'March':
                month = '03'
            if month == 'April':
                month = '04'
            if month == 'May':
                month = '05'
            if month == 'June':
                month = '06'
            if month == 'July':
                month = '07'
            if month == 'August':
                month = '08'
            if month == 'September':
                month = '09'
            if month == 'October':
                month = '10'
            if month == 'November':
                month = '11'
            if month == 'December':
                month = '12'    
            year = pubdate_long.split(" ")[2]
            time = pubdate_long.split(" ")[4]
            publication_date_str = day + " " + month + " " + year + " " + time
            
            publication_date = datetime.strptime(publication_date_str, '%d %m %Y %H:%M')
            publication_date = SAST.localize(publication_date) # check this works, doesn't on cmdline

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-2]
            item['spider_name'] = self.name
            item['publication_name'] = self.publication_name

            yield item

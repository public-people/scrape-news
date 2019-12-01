import scrapy


class ScrapenewsItem(scrapy.Item):
    publication_name = scrapy.Field()
    spider_name = scrapy.Field()
    url = scrapy.Field()
    scraped_date = scrapy.Field()
    byline = scrapy.Field()
    retrieved_at = scrapy.Field()
    published_at = scrapy.Field()
    title = scrapy.Field()
    body_html = scrapy.Field()
    file_name = scrapy.Field()

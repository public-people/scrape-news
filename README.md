# scrape-news

Scrape South African news to provide search with links to the original articles.

This is important because search engines make no guarantee of including all articles. It's important to be able to find news articles even if search engines didn't think they're worth indexing.

## Contribution

We need very broad coverage of news outlets. Contributed spiders are very welcome. Any South African news is welcome.

It's really easy to contribute spiders. Basically you can copy an existing spider and change the xpaths to find the elements we're extracting.

Ideally spiders should be driven from the outlet's sitemap. Ideally you'll find the sitemap from /robots.txt. If you don't find it there, try /sitemap.xml or /sitemap.txt. If you can't find a sitemap, use a crawling spider (you can copy from `thenewage`).

Send a pull request or get in touch.

Next, go get started at [Development](#development)

## Copyright of news content

We do not make news content available for public consumption. We simply store and index the news content and the original URL and publication date to provide search functionality similar to search engines. This project intends to provide better access to news on the publisher's website. It should be used to send readers to relevant news websites rather than to replace them.

## Development

### Set up your development environment

Clone this repository

```bash
git clone https://github.com/public-people/scrape-news.git
```

Create a Python 2 virtual environment for this project inside the cloned project directory (Note: your virtual environment program might not be called `pyvenv` -
```bash
cd scrape-news
pyvenv env
```

...




Run a scraper to check that your environment is working properly. The argument `since_lastmod` is the earliest sitemap file and page the scraper will include. The setting `ITEMS_PIPELINES` disables the pipeline we have configured which you don't need for just developing a spider.

```bash
scrapy crawl iol -s ITEM_PIPELINES="{}" -a since_lastmod=2018-04-30
```

If it's working correctly, it will output a lot of information:

e.g. after starting up it will find the sitemap and some articles that it will ignore in the sitemaps:

```
2018-05-03 18:21:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/robots.txt> (referer: None) ['cached']
2018-05-03 18:21:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/sitemap.xml> (referer: https://www.iol.co.za/robots.txt) ['cached']
2018-05-03 18:21:18 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/personal-finance/sitemap.xml> (referer: https://www.iol.co.za/sitemap.xml)
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/utmost-good-faith-is-the-cornerstone-of-insurance-14626128
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/facebooks-lesson-on-being-priced-for-perfection-14625488
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/six-cappuccinos-or-a-year-off-your-home-loan-14626132
```

when it reaches articles that are after the earliest accepted date, it will actually scrape content from the pages and print the resulting [ScrapenewsItem]() for the article

```
2018-05-03 18:21:34 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.iol.co.za/personal-finance/stanlib-may-further-reduce-fund-offering-14717297>
{'body_html': u'<div itemprop="articleBody" class="article-body" ... the ratings, De Klerk says.</p>\n<!-- C-ON- TEXT_CONTENT_END --></div></div>',
 'byline': u'Mark Bechard',
 'file_name': 'stanlib-may-further-reduce-fund-offering-14717297',
 'publication_name': 'IOL News',
 'published_at': '2018-04-30T15:04:00+02:00',
 'retrieved_at': '2018-05-03T16:21:31.603070',
 'spider_name': 'iol',
 'title': u'Stanlib may further reduce fund offering',
 'url': 'https://www.iol.co.za/personal-finance/stanlib-may-further-reduce-fund-offering-14717297'}
```


## Deployment

We use scrapyd to run the scrapers.

We use cron to schedule the scrapers regularly.

### Deploy a scraper to scrapyd

### Schedule a scraper

SitemapSpider scrapers can run daily, fetching only the latest articles. Crawling scrapers have to visit every page on the site so we only run them weekly.

Tunnel a connection to the server if you're not scheduling it from the server:

```
ssh -L 6800:localhost:6800 username@hostname
```

#### Schedule a SitemapSpider

SitemapSpiders take an argument `since_lastmod` which is an ISO format date filtering sitemaps and links in sitemaps. To do a complete scrape, just set it to a date very long ago, like `1900-01-01`.

```
curl -v http://localhost:6800/schedule.json -d project=scrapenews -d spider=iol -d setting=ALEPH_API_KEY=... -d since_lastmod=$(date +%Y-%m-%d -d "5 day ago")
```

#### Schedule a crawling spider

```
curl -v http://localhost:6800/schedule.json -d project=scrapenews -d spider=thenewage -d setting=ALEPH_API_KEY=...
```
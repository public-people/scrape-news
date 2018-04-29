# scrape-news

Scrape South African news to provide search with links to the original articles.

This is important because search engines make no guarantee of including all articles. It's important to be able to find news articles even if search engines didn't think they're worth indexing.

## Contribution

We need very broad coverage of news outlets. Contributed spiders are very welcome. Any South African news is welcome.

It's really easy to contribute spiders. Basically you can copy an existing spider and change the xpaths to find the elements we're extracting.

Ideally spiders should be driven from the outlet's sitemap. Ideally you'll find the sitemap from /robots.txt. If you don't find it there, try /sitemap.xml or /sitemap.txt. If you can't find a sitemap, use a crawling spider (you can copy from `thenewage`).

Send a pull request or get in touch.

## Copyright of news content

We do not make news content available for public consumption. We simply store and index the news content and the original URL and publication date to provide search functionality similar to search engines. This project intends to provide better access to news on the publisher's website. It should be used to send readers to relevant news websites rather than to replace them.

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
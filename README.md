# scrape-news

Scrape South African news to provide search with links to the original articles.

This is important because search engines make no guarantee of including all articles. It's important to be able to find news articles even if search engines didn't think they're worth indexing.

## Contribution

We need very broad coverage of news outlets. Contributed spiders are very welcome. Any South African news is welcome.

It's really easy to contribute spiders. Basically you can copy an existing spider and change the xpaths to find the elements we're extracting.

See the _In Progress_ column at [https://trello.com/b/9TVRB4gb/public-people](https://trello.com/b/9TVRB4gb/public-people) to see which publications are currently being tackled to avoid duplication.

Next, go get started at [Development](#development)

## Copyright of news content

We do not make news content available for public consumption. We simply store and index the news content and the original URL and publication date to provide search functionality similar to search engines. This project intends to provide better access to news on the publisher's website. It should be used to send readers to relevant news websites rather than to replace them.

## Requirements

- Python 3.5+
- Python virtual environment with packages installed from [requirements.txt](/requirements.txt). This main library used [Scrapy](https://scrapy.org/).
- Setup [scrapyd](https://scrapyd.readthedocs.io/en/stable/) (optional).
- Aleph account and credentials for uploading results (optional).

## Development

### Set up your development environment

#### Clone

Fork this repository on GitHub and clone your fork:

```bash
git clone https://github.com/your-name/scrape-news.git
```
or

```bash
git clone git@github.com:your-name/scrape-news.git
```

(Make sure to replace ```your-name```.)

Navigate to the repo.

```bash
$ cd <PATH_TO_REPO>
```

### Make commands

This project comes with a [Makefile](/Makefile), to run with `make` command.

```bash
$ make
```

We'll use some of those below.

### Setup virtual environment

1. Create a virtual environment called `venv`.
    ```bash
    $ make new-env
    ```
2. Activate it.
    ```bash
    $ source venv/bin/activate
    ```
3. Install main dependencies.
    ```bash
    $ make install
    ```
4. Install dev dependencies.
    ```bash
    $ make dev-install
    ```

### Run

Note: Always activate the project's environment before using it.

```bash
$ source venv/bin/activate
```

#### List available spiders in the project

```bash
$ make list
businesslivecrawl
businesslivesitemap
dailymaverick
dailyvoice
dfa
dispatchlive
enca
ewn
groundup
iol
mg
news24
rekordnorth
sabc
sowetanlive
thenewage
timeslive
```

We will use these crawler names in the next step. Note that these names are generated from _classes_ in the [spiders](/scrapenews/spiders/) directory and not the _filenames_.

#### Run scraper

Run a scraper using the command below to check that your environment is working properly. This can be done from the project root because of how the `scrapy` library works.

If you need to get a template crawl command quickly and then fill in with a crawler, run the following and then copy and paste the result to a new line.

```bash
$ make quickstart
scrapy crawl -s ITEM_PIPELINES="{}" -a since_lastmod=2018-01-01 <CRAWLER>
```

For example, run the command using the _iol_ spider.

```bash
$ scrapy crawl -s ITEM_PIPELINES="{}" -a since_lastmod=2018-04-30 iol
```

The arguments for the above command are required. Here is how to use them:

- The setting `ITEM_PIPELINES` disables the pipeline we have configured which you don't need for just developing a spider.
- The argument `since_lastmod` is the earliest sitemap file and page the scraper will include.
- The last argument `crawl` is the name of the scraper (e.g. `iol`). See output from the previous section.

For quick testing on the _iol_ spider, a shortcut for the above command has been added to the [Makefile](/Makefile).

```bash
$ make test-iol
```

#### Output

If the crawl command is working correctly, it will output a lot of information.

e.g. after starting up it will find the sitemap and some articles that it will ignore in the sitemaps.

Sample output for _iol_ crawler:
```
2018-05-03 18:21:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/robots.txt> (referer: None) ['cached']
2018-05-03 18:21:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/sitemap.xml> (referer: https://www.iol.co.za/robots.txt) ['cached']
2018-05-03 18:21:18 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.iol.co.za/personal-finance/sitemap.xml> (referer: https://www.iol.co.za/sitemap.xml)
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/utmost-good-faith-is-the-cornerstone-of-insurance-14626128
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/facebooks-lesson-on-being-priced-for-perfection-14625488
2018-05-03 18:21:18 [scrapenews.spiders.sitemap] DEBUG: Skipping too old https://www.iol.co.za/personal-finance/six-cappuccinos-or-a-year-off-your-home-loan-14626132
```

when it reaches articles that are after the earliest accepted date, it will actually scrape content from the pages and print the resulting [ScrapenewsItem](/scrapenews/items.py) for the article:

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


### Code checks

To maintain Python code quality, **linting** and **unit tests** should be run locally and on Github. Linting give you style warnings. The unit tests are in the [unit](/tests/unit) directory and run tests against the project code.

#### Local

Run the checks locally using the following commands:

```bash
$ make lint
```

```bash
$ make unit
```

#### Github

Linting and tests areas are run automatically on Github Actions when you do a push using the [Python workflow](/.github/workflows/pythonapp.yml) config. View the results on a Github repo under the _Actions_ tab.


### Make a spider

Public People needs the following fields:

| field | description |
|-------|-------------|
| body_html | An HTML string that contains all the text of the article and any other content the publication had in the article body. Don't bother filtering ads or anything - just try and exclude headers and footers and make sure you have the entire article, even if it's broken into multiple sections on the page. |
| byline | String of all the authors' names and surnames as presented on the article page. |
| file_name | Usually the "slug" of the article in the URL. Some simple clear name for the article if it was a file. |
| publication_name | e.g. News24 - this can usually be hardcoded in the scraper and doesn't need to be scraped from the page. |
| published_at | ISO 8601 date - could even be partial, like just the year-month-date part excluding time. There's often a meta tag or an attribute on the element in the content where the date is for search engines - that value is often already in ISO 8601 format. |
| retrieved_at | ISO 8601 date of current date/time to know when we scraped it. |
| spider_name | Generally the module name. |
| title | Article title. |
| url | This is used as the unique identifier for this article for deduplication, so use the [canonical url meta tag value](https://yoast.com/rel-canonical/) if available, otherwise just try to parse out the unique part of the URL from `response.url` and exclude things like query string parameters and URL fragment  identifier. |

First, add this repository as a remote and make sure your local master is up to date:
```bash
git remote add upstream git@github.com:public-people/scrape-news.git
git fetch upstream
git checkout master
git merge upstream/master
```

Create and check out a branch for the spider you're making:
```bash
git checkout -b newssite
```
(Replace ```newssite``` with the name of the publication you're making a spider for.)

Ideally spiders should be driven from the outlet's sitemap. Ideally you'll find the sitemap from /robots.txt. If you don't find it there, try /sitemap.xml or /sitemap.txt.

If the ```newssite``` uses a _useful_ sitemap index (see for example [https://www.timeslive.co.za/sitemap/](https://www.timeslive.co.za/sitemap/)), use a sitemap spider.

If the sitemap index is less useful (see for example [https://www.dailyvoice.co.za/sitemap.xml](https://www.dailyvoice.co.za/sitemap.xml)), or if there isn't a sitemap index (or no sitemap at all), use a crawling spider.

Copy a spider from the repository and amend it as necessary: a good example of a sitemap spider is [iol](https://github.com/public-people/scrape-news/blob/master/scrapenews/spiders/iol.py); a good example of a crawling spider is [dfa](https://github.com/public-people/scrape-news/blob/master/scrapenews/spiders/dfa.py)).

### Test your responses

To test individual xpath or css responses you can use the scrapy shell:

```bash
scrapy shell "https://www.newssite.co.za/article-url"
```

If you go to the same url in your browser and right-click on, say, the title of the article, and select 'Inspect Element (Q)', you'll see something like this highlighted.

```html
<h1 class="article-title">Title of article</h1>
```

In the scrapy, shell you can then enter

```bash
>>> response.css('h1.article-title').xpath('text()').extract_first()
```
to get the title.

Now that you've checked that this works and doesn't have some unintended consequence, you can copy it into the relevant part of your spider; in this case:
```python
def parse(self, response):
    ...
    title = response.css('h1.article-title').xpath('text()').extract_first()
    ...
```

#### Do not use xpath for css classes

You could have also used the xpath in the above, but the preference is to use css lookup for classes. e.g.:

```bash
>>> response.xpath('//h1/[@class="article-title"]/text()').extract_first()
```

The reason for this is that xpaths can be brittle in more complicated instances. Consider the case of
```html
<div class="byline pin-right">John Smith</div>
```
The only way an xpath query will work here is if you give the exact class name:
```bash
>>> response.xpath('//div/[@class="byline pin-right"]/text()').extract_first()
```
which means that if the same publication uses, say, ```byline pin-left``` for certain articles the spider won't get a response for 'byline'.
(And if you were using ```extract()``` instead of ```extract_first()``` it would get an error.)
The safer option is therefore to use the following instead:
```bash
>>> response.css('div.byline').xpath('text()').extract_first()
```

#### Test and improve

Once you have all your paths figured out (fun, right? – have a look at the existing spiders for ideas on how to get around any issues you encounter, or shout on Slack), you can run it a couple of times to check that it works as expected and refine it. This is especially important for crawling spiders.

Exit from the scrapy shell (```Ctrl+D```) and run your spider:
```bash
scrapy crawl newssite -s ITEM_PIPELINES="{}" -a since_lastmod=2018-04-30
```
(Don't include the ```since_lastmod``` specification if it's a crawling spider.)

If it runs, yay! But the odds are that there will be some errors thrown; so search for the word 'error' in your output and see if you can figure out what's causing it – there's usually a pattern.

Another thing to look out for is 'ignoring': if the urls being ignored by your spider follow a pattern, consider adding some paths to 'deny' instead to save resources.

#### Make a pull request

Once your spider is done and ready for review, ```git add``` it and ```commit``` the change to your working branch.

Then, first make sure your local master is up to date:
```bash
git fetch upstream
git checkout master
git merge upstream/master
```
and merge any changes into your working branch:
```bash
git merge master newssite
```

Then push your ```newssite``` branch to your fork on GitHub (use ```git remote -v``` to check the names of your remotes):
```bash
git push origin newssite
```
Go to [Pull requests](https://github.com/public-people/scrape-news/compare), choose to 'compare across forks', and compare the ```base fork: public-people/scrape-news```, ```base: master``` to ```head fork: your-name/scrape-news```, ```compare: newssite```, and make a new pull request!

If you make some changes to your spider after your initial pull request, do the following to update the PR:
```bash
# check you're up to date
git fetch upstream
git checkout master
git merge upstream/master
git merge master newssite

# push your changes
git checkout newssite
git add newssite.py
git commit -m "Make changes to newssite spider to incorporate/address review comments"
git push origin newssite
```

If ```git fetch upstream``` doesn't return anything you can skip the next steps until checking out your ```newssite``` branch.

Pushing the same branch again will automatically update your existing PR.

## Deployment

We use scrapyd to run the scrapers.

We use cron to schedule the scrapers regularly.

### Deploy a scraper to scrapyd

`scrapyd-deploy`

### Schedule a scraper

SitemapSpider scrapers can run daily, fetching only the latest articles. Crawling scrapers have to visit every page on the site so we only run them weekly.

Tunnel a connection to the server if you're not scheduling it from the server:

```bash
ssh -L 6800:localhost:6800 username@hostname
```

#### Schedule a SitemapSpider

SitemapSpiders take an argument `since_lastmod` which is an ISO format date filtering sitemaps and links in sitemaps. To do a complete scrape, just set it to a date very long ago, like `1900-01-01`.

```bash
curl -v http://localhost:6800/schedule.json -d project=scrapenews -d spider=iol -d setting=ALEPH_API_KEY=... -d since_lastmod=$(date +%Y-%m-%d -d "5 day ago")
```

#### Schedule a crawling spider

```bash
curl -v http://localhost:6800/schedule.json -d project=scrapenews -d spider=thenewage -d setting=ALEPH_API_KEY=...
```

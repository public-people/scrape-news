import scrapy
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.http import Request
import logging

logger = logging.getLogger(__name__)


class SitemapSpider(scrapy.spiders.SitemapSpider):

    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning("Ignoring invalid sitemap: %(response)s",
                               {'response': response}, extra={'spider': self})
                return

            s = Sitemap(body)
            if s.type == 'sitemapindex':
                for loc in iterloc(s, self.since_lastmod, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                for loc in iterloc(s, self.since_lastmod, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield Request(loc, callback=c)
                            break


def iterloc(it, since_lastmod, alt=False):
    for d in it:
        if d.get('lastmod', None) is None or d['lastmod'] > since_lastmod:
            yield d['loc']
        else:
            logger.debug("Skipping too old %s", d['loc'])

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                if d.get('lastmod', None) is None or d['lastmod'] > since_lastmod:
                    yield l
                else:
                    logger.debug("Skipping too old %s", d['loc'])

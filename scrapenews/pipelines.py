# -*- coding: utf-8 -*-
import logging
import requests
import json
from urllib.parse import urljoin
from slugify import slugify
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


TIMEOUT_SECONDS = 10


class ZANewsPipeline(object):

    def __init__(self, zanews_token, zanews_host):
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'Token %s' % zanews_token
        self.host = zanews_host
        self.session.mount(self.host, HTTPAdapter(max_retries=5))
        self._publications = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            zanews_token=crawler.settings.get('ZANEWS_TOKEN'),
            zanews_host=crawler.settings.get('ZANEWS_HOST'),
        )

    def process_item(self, item, spider):
        publication_url = self.get_publication_url(item['publication_name'])

        meta = {
            'spider_name': item['spideor_name'],
            'published_url': item['url'],
            'title': item['title'],
            'retrieved_at': item['retrieved_at'],
            'published_at': item['published_at'],
            'body_html': item['body_html'],
            'byline': item[:'byline'],
            'publication': publication_url,
        }

        url = self.make_url('articles')

        logger.info("Sending '%s' to %s", item['title'], url)
        logger.debug("meta = %r", meta)

        r = self.session.post(
            url,
            data={'meta': json.dumps(meta)},
            timeout=TIMEOUT_SECONDS,
        )

        if r.status_code == 200:
            return item

        if (r.status_code == 400 and "already exists" in r.json().get('published_url', [''])[0]):
            logger.info("Already archived %s", item["published_url"])
            return item

        logger.error("%s\n%s", r.status_code, r.text)
        r.raise_for_status()

    def make_url(self, path):
        prefix = urljoin(self.host, '/api/')
        return urljoin(prefix, path)

    def get_publication_url(self, name):
        slug = slugify(name)
        publication = self.get_publications().get(slug, None)
        if not publication:
            self.create_publication(name, slug)
            publication = self.get_publications(refresh=True)
        if publication:
            return publication['url']
        else:
            raise Exception("Can't find publication %s" % slug)

    def get_publications(self, refresh=False):
        if self._publications and not refresh:
            return self._publications
        url = self.make_url('publications')
        self._publications = load_publications(self.session, {}, url)
        return self._publications

    def create_publication(self, name, slug):
        publication = {
            "name": name,
            "slug": slug,
        }
        url = self.make_url('publications')
        r = self.session.post(url, publication)
        r.raise_for_status()


def load_publications(session, publications, url):
    """
    resursively load publications until all pages have been added to the
    provided dictionary
    """
    result = session.get(url, timeout=TIMEOUT_SECONDS)
    result.raise_for_status()
    for pub in result.json()['results']:
        publications[pub['slug']] = pub
    next_url = result.json()['next']
    if next_url:
        return load_publications(publications, next_url)
    else:
        return publications

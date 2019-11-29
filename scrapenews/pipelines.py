# -*- coding: utf-8 -*-
import logging
import requests
import json
from urlparse import urljoin
from slugify import slugify
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


class AlephPipeline(object):

    def __init__(self, api_key, aleph_host):
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'apikey %s' % api_key
        self.aleph_host = aleph_host
        self.session.mount(self.aleph_host, HTTPAdapter(max_retries=5))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            api_key=crawler.settings.get('ALEPH_API_KEY'),
            aleph_host=crawler.settings.get('ALEPH_HOST'),
        )

    def process_item(self, item, spider):
        if self.url_is_already_indexed(item['url']):
            logger.info("Not ingesting already indexed %s", item['url'])
            return item

        meta = {
            'crawler': item['spider_name'],
            'source_url': item['url'],
            'title': item['title'],
            'file_name': item['file_name'],
            'extension': 'html',
            'encoding': 'utf-8',
            'foreign_id': item['url'],
            'mime_type':  'text/html',
            'countries': ['za'],
            'retrieved_at': item['retrieved_at'],
            'published_at': item['published_at'],
        }

        collection_id = self.get_collection_id(
            slugify(unicode(item['publication_name'])),
            item['publication_name']
        )
        url = self.make_url('collections/%s/ingest' % collection_id)

        logger.info("Sending '%s' to %s", item['title'], url)
        logger.debug("meta = %r", meta)

        r = self.session.post(
            url,
            data={'meta': json.dumps(meta)},
            files={'file': item['body_html']},
            timeout=10,
        )
        if not r.status_code == requests.codes.ok:
            logger.error("%s\n%s", r.status_code, r.text)
        r.raise_for_status()

        return item

    def get_collection_id(self, foreign_id, name):
        url = self.make_url('collections')
        r = self.session.get(url, timeout=10, params={
            'filter:foreign_id': foreign_id
        })
        r.raise_for_status()
        data = r.json()
        for coll in data.get('results'):
            if coll.get('foreign_id') == foreign_id:
                return coll.get('id')

        r = self.session.post(url, json={
            'label': name,
            'category': 'news',
            'managed': True,
            'foreign_id': foreign_id
        })
        r.raise_for_status()
        return r.json().get('id')

    def make_url(self, path):
        prefix = urljoin(self.aleph_host, '/api/2/')
        return urljoin(prefix, path)

    def url_is_already_indexed(self, source_url):
        logger.info("Checking if already indexed: %s", source_url)
        url = self.make_url('documents')
        r = self.session.get(url, params={'filter:source_url': source_url}, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data['total'] not in (0, 1):
            raise Exception(("Unexpected number of existing documents (%r) for %s"
                             "\nrequested %r")
                            % (data['total'], source_url, r.url))
        return data['total'] == 1

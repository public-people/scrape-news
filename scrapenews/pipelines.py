# -*- coding: utf-8 -*-
import dateutil.parser
import logging

logger = logging.getLogger(__name__)


class ScrapenewsPipeline(object):
    def process_item(self, item, spider):

        publication_date = dateutil.parser.parse(item['publication_date'])

        logger.info("%r\n%r", publication_date, item)
        return item

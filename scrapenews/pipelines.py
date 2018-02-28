# -*- coding: utf-8 -*-
import dateutil.parser
import logging
from scrapenews.models import Article
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://sanews@localhost/sanews')
logger = logging.getLogger(__name__)


class ScrapenewsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        publication_date = dateutil.parser.parse(item['publication_date'])

        session = self.Session()
        article = Article(
            url=item['url'],
            publication_date=item['publication_date'],
            publication_name=item['publication_name'],
            byline=item['byline'],
            title=item['title'],
            body_html=item['body_html'],
        )

        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

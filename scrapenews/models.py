from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime
import sqlalchemy.sql.functions as func


Base = declarative_base()


class Article(Base):
    """
    Data about a gazette that was scraped from the web
    """
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    url = Column(String,
                 unique=True,
                 nullable=False)
    publication_name = Column(String,
                              nullable=False)
    byline = Column(String,
                    nullable=False,
                    index=True)
    publication_date = Column(Date,
                              nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.current_timestamp())
    body_html = Column(String,
                       nullable=False)
    title = Column(String,
                   nullable=False,
                   index=True)

    def __repr__(self):
        return "<Article(url=%r, title='%s')>" % (self.url, self.title)

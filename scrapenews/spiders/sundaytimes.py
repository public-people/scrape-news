# -*- coding: utf-8 -*-

from scrapenews.spiders.timeslive import TimesliveSpider


class SundayTimesSpider(TimesliveSpider):
    """
    Class implementing a sitemap spider for the Sunday Times (https://www.timeslive.co.za/sunday-times/).
    The Sunday Times is hosted on the TimesLIVE website (https://www.timeslive.co.za).
    This spider is therefore implemented as a subclass of the TimesLIVE spider but only parsing paths that contain `/sunday-times/`.
    """

    name = 'sundaytimes'

    sitemap_rules = [('/sunday-times/', 'parse')]

    publication_name = 'Sunday Times'

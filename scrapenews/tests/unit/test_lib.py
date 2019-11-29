from __future__ import absolute_import
import datetime
from unittest import TestCase

import lib


class TestLib(TestCase):

    def test_parse_date(self):
        publication_date_str = "2019-11-22T09:10:11.000Z"
        result = lib.parse_date(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22))

        publication_date_str = "2019-11-22 09:10:11.000Z"
        result = lib.parse_date(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22))

        publication_date_str = "2019-11-22"
        result = lib.parse_date(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22))

        publication_date_str = "\t 2019-11-22T09:10:11.000Z \t"
        result = lib.parse_date(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22))

    def test_parse_date_hour_min(self):
        publication_date_str = "2019-11-22T09:10:11.000Z"
        result = lib.parse_date_hour_min(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10))

        publication_date_str = "2019-11-22 09:10:11.000Z"
        result = lib.parse_date_hour_min(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10))

        publication_date_str = "2019-11-22T09:10"
        result = lib.parse_date_hour_min(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10))

        publication_date_str = "2019-11-22 09:10"
        result = lib.parse_date_hour_min(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10))

    def test_parse_date_hour_min_sec(self):
        publication_date_str = "2019-11-22T09:10:11.000Z"
        result = lib.parse_date_hour_min_sec(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10, 11))

        publication_date_str = "2019-11-22T09:10:00"
        result = lib.parse_date_hour_min_sec(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10, 0))

        publication_date_str = "2019-11-22 09:10:00"
        result = lib.parse_date_hour_min_sec(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 22, 9, 10, 0))

    def test_parse_long_date_time(self):
        publication_date_str = "27 November 2019, 6:43 PM"
        result = lib.parse_long_month_hour_min_meridian(publication_date_str)
        self.assertEqual(result, datetime.datetime(2019, 11, 27, 18, 43, 0))

        publication_date_str = "3 April 2000, 1:22 AM"
        result = lib.parse_long_month_hour_min_meridian(publication_date_str)
        self.assertEqual(result, datetime.datetime(2000, 4, 3, 1, 22, 0))

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

from __future__ import absolute_import
import datetime


def parse_date(value):
    return datetime.datetime.strptime(value[:10], '%Y-%m-%d')


def parse_date_hour_min(value):
    value = value.replace("T", " ")
    return datetime.datetime.strptime(value[:16], '%Y-%m-%d %H:%M')


def parse_date_hour_min_sec(value):
    """
    Ignore parse datetime string down to seconds, ignoring microseconds.
    """
    value = value.replace("T", " ")
    return datetime.datetime.strptime(value[:19], '%Y-%m-%d %H:%M:%S')


def parse_long_month_hour_min_meridian(value):
    return datetime.datetime.strptime(value, '%d %B %Y, %I:%M %p')

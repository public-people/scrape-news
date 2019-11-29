import datetime


def parse_date(value):
    return datetime.datetime.strptime(value[:10], '%Y-%m-%d')


def parse_date_hour_min(value):
    return datetime.datetime.strptime(value[:16], '%Y-%m-%dT%H:%M')


def parse_date_hour_min_sec(value):
    """
    Ignore parse datetime string down to seconds, ignoring microseconds.
    """
    return datetime.datetime.strptime(value[:19], '%Y-%m-%dT%H:%M:%S')

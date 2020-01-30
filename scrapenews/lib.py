import datetime


def parse_date(value):
    return datetime.datetime.strptime(value.strip()[:10], '%Y-%m-%d')


def parse_date_hour_min(value):
    value = value.replace("T", " ")
    return datetime.datetime.strptime(value.strip()[:16], '%Y-%m-%d %H:%M')


def parse_ISO8601_datetime(value):
    """
    Ignore parse datetime string down to seconds, ignoring microseconds.
    """
    value = value.replace("T", " ")
    return datetime.datetime.strptime(value.strip()[:19], '%Y-%m-%d %H:%M:%S')


def parse_long_month_hour_min_meridian(value):
    return datetime.datetime.strptime(value.strip(), '%d %B %Y, %I:%M %p')

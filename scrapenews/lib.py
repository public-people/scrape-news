import datetime


def parse_date(value):
    return datetime.datetime.strptime(value[:10], '%Y-%m-%d')


# import lib
def parse_date_hours_minutes(value):
    return datetime.datetime.strptime(value[:16], '%Y-%m-%dT%H:%M')

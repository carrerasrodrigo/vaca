import datetime

from dateutil.relativedelta import relativedelta


def fdate(f='%Y-%m-%d', d=datetime.datetime.now()):
    return d.strftime(f)


def date(*args, **kwargs):
    return datetime.datetime(*args, **kwargs)


def fdatetime(f='%Y-%m-%d %H:%M:%S', d=datetime.datetime.now()):
    return d.strftime(f)


def datetime_range(start, end, date_range=dict(days=1)):
    d = start
    while d <= end:
        yield d
        d += relativedelta(**date_range)

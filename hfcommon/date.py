# -*- coding: utf-8 -*-

import datetime
import dateutil.parser

import arrow
from .format import conversion, DATETIME_FORMAT


def human_date_full(handler, ts, with_time=False):
    translate = handler.locale.translate

    today = datetime.datetime.today().date()
    yesterday = today - datetime.timedelta(1)
    if isinstance(ts, basestring):
        if ts.index('-'):
            local = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        else:
            local = datetime.datetime.fromtimestamp(ts)
    else:
        local = ts

    if today == local.date():
        result = translate('date.today')
    elif yesterday == local.date():
        result = translate('date.yesterday')
    else:
        return u'{} {} {}'.format(
            local.day,
            translate('genitive.month.{}'.format(local.month)),
            local.year if local.year != today.year else '',
        )

    if with_time:
        return u'{} {} {}'.format(result, translate('date.at'), "{:%H:%M}".format(local))

    return result


def fulltime(value, trl):
    now = datetime.date.today()
    d = arrow.get(value, DATETIME_FORMAT)

    return u'{} · {} {} {}'.format(
        d.format('HH:mm'), d.format('DD'), trl(u'genitive.month.{}'.format(d.format('M'))),
        d.format('YYYY') if now.year != d.year else '')


def age(day, month, year):
    if day and not month and not year:
        d = day.split(' ')[0].split('-')
        day = int(d[0])
        month = int(d[1])
        year = int(d[2])

    today = datetime.date.today()
    born = datetime.date(year, month, day)

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def days(day, month=None, year=None):
    today = datetime.datetime.today().date()
    if month is None and year is None:
        local = datetime.datetime.strptime(day, "%Y-%m-%d %H:%M:%S").date()
    else:
        local = datetime.date(year, month, day)

    return abs((local - today).days)


def months_to_work_period(months):
    return months / 12, months % 12


def work_period(trl, f, t):
    if not f:
        return

    if isinstance(f, int):
        years, months = months_to_work_period(f)
    else:
        if isinstance(f, basestring):
            splitted = f.split(' ')
            d = splitted[0].split('-')

            month = int(d[1])
            year = int(d[0])

            f = datetime.date(year, month, 1)
        if t:
            if isinstance(t, basestring):
                splitted = t.split(' ')
                d = splitted[0].split('-')

                month = int(d[1])
                year = int(d[0])

                t = datetime.date(year, month, 1)
        else:
            t = datetime.date.today()

        months = (t.year - f.year) * 12
        months -= (f.month - 1)  # previous months (not inclusive)
        months += t.month  # to months (inclusive)

        months = 0 if months <= 0 else months
        years = int(months/12)
        months -= years * 12

    return u'{} {}'.format(
        u'{} {}'.format(years, trl('age.{}'.format(conversion(years)))) if years > 0 else '',
        u'{} {}'.format(months, trl('month.{}'.format(conversion(months)))) if months > 0 else ''
    ).strip()


def to_date(val):
    dt = from_isoformat(val) if isinstance(val, basestring) else from_unixtime(val)
    return '{}-{}-{}'.format(dt.year, dt.month, dt.day)


def from_isoformat(val):
    return dateutil.parser.parse(val)


def from_unixtime(val):
    return datetime.datetime.fromtimestamp(val)

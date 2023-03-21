# -*- coding: utf-8 -*-
import re
import phonenumbers
import arrow
from .util import find


DATETIME_FORMAT = 'YYYY-MM-DD HH:mm:ss'
DATE_FORMAT = 'YYYY-MM-DD'

_endings = [2, 0, 1, 1, 1, 2]  # для 0 будет возвращено окончание "много", например, 0 вакансий


def number_ending(number):
    return 2 if 20 > number % 100 > 4 else _endings[min(number % 10, 5)]


def conversion(num):
    if num == 0:
        return 'zero'
    elif isinstance(num, float):
        return 'many'

    return ['one', 'some', 'many'][number_ending(num)]


_THOUSANDS_RE = r'\B(?=(?:\d{3})+$)'


def thousands(s, thousands_sep=' ', decimal_sep='.'):
    try:
        s = str(s)
    except UnicodeEncodeError:
        # needed for PY2 cases like s = u'1000 руб'
        pass

    sp = s.split(decimal_sep)
    decimal = sp[1] if len(sp) > 1 else None
    val = re.sub(_THOUSANDS_RE, thousands_sep, sp[0])
    return val + ((decimal_sep + decimal) if decimal is not None else '')


def phone(s):
    if isinstance(s, dict):
        if s.get('country') and s.get('city') and s.get('number'):
            value = '+{}{}{}'.format(s['country'], s['city'], s['number'])
        else:
            value = s.get('formatted')
    else:
        value = s

    try:
        split = re.split(r'^([\+0-9a-zA-Z\(\)\-\s]+)', value)
        formatted = phonenumbers.format_number(phonenumbers.parse(split[1].strip(), 'RU'),
                                               phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return '{}{}{}'.format(formatted, ' ' if split[2] else '', split[2])
    except Exception as e:
        return value


def clean_phone(s):
    if isinstance(s, dict):
        value = '+{}{}{}'.format(s['country'], s['city'], s['number'])
    else:
        value = s

    try:
        split = re.split(r'^([\+0-9a-zA-Z\(\-\s]+)', value)
        formatted = phonenumbers.format_number(phonenumbers.parse(split[1].strip(), 'RU'),
                                               phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return formatted.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    except Exception as e:
        return value


def format_timezone(timezone):
    t = arrow.get().replace(tzinfo=timezone).format('Z')

    return 'UTC{}:{}'.format(t[:3], t[-2:]).strip()


def calendar_period(_, start, end, all_day, local=False):
    start_date = arrow.get(start)
    end_date = arrow.get(end)

    same_day = start_date.date() == end_date.date()

    result = u'{} {} {}'.format(start_date.format('D'), _('genitive.month.{}'.format(start_date.format('M'))),
                                start_date.format('YYYY'))

    start_time = None

    if not all_day:
        if same_day:
            result += u','

        start_time = start_date.format('HH:mm')
        result += u' ' + start_time

    end_time = end_date.format('HH:mm')

    if (not all_day and start_time != end_time) or not same_day:
        result += u' — '

    if not same_day:
        result += u'{} {} {}'.format(end_date.format('D'), _('genitive.month.{}'.format(end_date.format('M'))),
                                     end_date.format('YYYY'))
        result += u'' if all_day else u' '

    if not all_day and start_time != end_time:
        result += end_time

    return result.strip()


def day_of_week(day):
    parsed = arrow.get(day)
    return int(parsed.format('d'))


def deep_value(value_id, values):
    result = []

    def find_value(id):
        div = find(values, lambda x: x['id'] == id)
        if div:
            result.append(div['name'])

            if div['parent']:
                find_value(div['parent'])

    find_value(value_id)

    return u' · '.join(result)

# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import datetime
import time
try:
    from types import SimpleNamespace
except:
    class SimpleNamespace(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def __repr__(self):
            keys = sorted(self.__dict__)
            items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
            return "{}({})".format(type(self).__name__, ", ".join(items))

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

from logging import getLogger
log = getLogger(__name__)


class TimeUtils():

    @staticmethod
    def str_to_date(date_string, default=False):
        if type(date_string) == datetime.date:
            return date_string

        if type(date_string) == datetime.datetime:
            return date_string.date()

        try:
            return datetime.datetime(*time.strptime(str(date_string)[:10], "%Y-%m-%d")[:6]).date()
        except Exception as e:
            log.error(e, exc_info=True)
            return default


    @staticmethod
    def str_to_datetime(date_string, time_part = ' 00:00:00', default=False):
        if type(date_string) == datetime.datetime:
            return date_string

        l = len(date_string)
        if l < 19:
            r = 19-l
            date_string = date_string+time_part[0-r:]

        try:
            return datetime.datetime.strptime(str(date_string)[:19], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            log.error(e)
            return default


    @staticmethod
    def date_diff(date_from, date_to):
        duration = date_to - date_from
        duration_in_s = duration.total_seconds()

        x = SimpleNamespace()

        x.years = int(divmod(duration_in_s, 31556926)[0])
        x.days = int(divmod(duration_in_s, 86400)[0])
        x.hours = int(divmod(duration_in_s, 3600)[0])
        x.minutes = int(divmod(duration_in_s, 60)[0])
        x.seconds = int(duration_in_s)
        x.microseconds = int(duration.microseconds)
        return x

    @staticmethod
    def set_last_day(date):
        date = TimeUtils.str_to_date(date)
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

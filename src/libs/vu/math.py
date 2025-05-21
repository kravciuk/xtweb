# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from decimal import Decimal, ROUND_HALF_UP


class Math:

    @staticmethod
    def round(value, point='.01'):
        value = Decimal(str(value))
        return Decimal(value.quantize(Decimal(point), rounding=ROUND_HALF_UP))

    @staticmethod
    def percent(amount, percent, point='.01'):
        return Math.round(amount / 100 * percent, point)

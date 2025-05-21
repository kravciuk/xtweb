# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', _(u'Only alphanumeric characters A-Z, a-z, 0-9 are allowed.'))
alphanumeric_space = RegexValidator(r'^[0-9a-zA-Z ]*$', _(u'Only alphanumeric characters A-Z, a-z, 0-9 and space are allowed.'))
alphanumeric_dash = RegexValidator(r'^[0-9a-zA-Z-]*$', _(u'Only alphanumeric characters A-Z, a-z, 0-9 and dash are allowed.'))

def greater_than_zero(value):
    if value < 0:
        raise ValidationError('The value should be greater or equal zero.', code='min_value_eq')

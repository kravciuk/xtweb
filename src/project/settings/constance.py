# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

_ = lambda s: s

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'DEFAULT_EMAIL': ('admin@localhost.local', 'Default admin e-mail', str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    _(u'General options'): ('DEFAULT_EMAIL', ),
}

# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from . import VAR_DIR

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(VAR_DIR, 'local.db'),
        "HOST": os.getenv('DB_HOST', '___host__'),
        'NAME': os.getenv('DB_NAME', '__db_name_'),
        'USER': os.getenv('DB_LOGIN', '__user__'),
        'PASSWORD': os.getenv('DB_PASS', '__password__'),
    }
}

CONN_MAX_AGE = 60

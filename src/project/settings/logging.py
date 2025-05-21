# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from . import VAR_DIR
LOG_DIR = VAR_DIR+'/logs'

# Configure logging
# -----------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] -> %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '(%(name)s:%(lineno)s) %(message)s'
        },
        'extended': {
            'format': '%(levelname)s:%(name)s: %(message)s '
            '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'null': {
            "class": 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR+'/errors.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 7,
            'formatter': 'extended',
        },
        'trash_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR+'/trash_error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 7,
            'formatter': 'extended',
        },
    },
    'loggers': {
        'PIL': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['trash_error'],
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

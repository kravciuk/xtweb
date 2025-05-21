# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from kombu import Exchange, Queue

CELERY_TIMEZONE = "Europe/Vilnius"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '1')

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'queue_order_strategy': 'priority',
    'priority_steps': list(range(10)),
    'sep': '.',
}

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = {
    'default': Queue('default', Exchange('default'), routing_key='default'),
}

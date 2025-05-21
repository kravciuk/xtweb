# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
import logging.config

from django.conf import settings
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_default_queue = 'medium'
app.autodiscover_tasks()


# configure celery logging
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('celery')

@task_prerun.connect
def task_start_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **extra):
    logger.info(f'Task started: {task.name} [ID: {task_id}]')

@task_postrun.connect
def task_success_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, **extra):
    logger.info(f'Task finished: {task.name} [ID: {task_id}]')

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, exc=None, traceback=None, **extra):
    logger.error(f'Task failed: {task.name} [ID: {task_id}] - Exception: {exc}')

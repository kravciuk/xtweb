# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import time
from uwsgidecorators import spool

from .models import Example

import logging
log = logging.getLogger(__name__)


@spool(pass_arguments=True)
def example_task(*args, **kwargs):
    log.debug('Task "example_task" started.')
    print(args)
    print(kwargs)
    print(Example.objects.get(pk=kwargs['pk']))
    time.sleep(kwargs['delay'])
    log.debug('Task "example_task" ended.')

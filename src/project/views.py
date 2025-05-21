# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

import logging
log = logging.getLogger(__name__)


def error404(request, exception):
    context = {
        'title': 'Page not found',
        'text': 'Page not found',
    }

    log.debug(exception)

    return render(request, '404.html', context, status=404)


def index_page(request):
    return redirect('/%s/' % settings.LANGUAGE_CODE)

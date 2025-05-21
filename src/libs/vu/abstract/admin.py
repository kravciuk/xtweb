# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Example

from logging import getLogger
log = getLogger(__name__)


class ExampleAdmin(admin.ModelAdmin):
    list_display = []
    list_filter = []
    search_fields = []
    autocomplete_fields = []


admin.site.register(Example, ExampleAdmin)

# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType

from vu.abstract.models import Base


class Comment(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    ip_v4 = models.CharField(max_length=15)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_pk = models.IntegerField()
    approved = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    comment = models.TextField()

    def __str__(self):
        return ''


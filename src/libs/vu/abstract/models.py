# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import datetime
import os
import uuid
from hashids import Hashids

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import FileField, ImageField
from django.contrib.auth import get_user_model

from logging import getLogger
log = getLogger(__name__)

User = get_user_model()


def unique_file_name(dir_path, file_name):
    if not os.path.exists("%s/%s" % (dir_path, file_name)):
        return file_name
    else:
        _file, _ext = os.path.splitext(file_name)
        i = 1
        while os.path.exists("%s/%s_%s%s" % (dir_path, _file, str(i), _ext)):
            i += 1
        return "%s_%s%s" % (_file, str(i), _ext)


def unique_slug(instance, slug_field, slug, counter=0, query=None):
    if counter > 0:
        test_slug = "%s_%s" % (slug, counter)
    else:
        test_slug = slug

    rs = instance.objects.filter(**{slug_field: test_slug})
    if query:
        rs = rs.filter(**query)
    if rs[:1]:
        counter += 1
        return unique_slug(instance, slug_field, slug, counter, query)
    else:
        return test_slug


class UniqueFileField(FileField):
    def generate_filename(self, instance, filename):
        _name, ext = os.path.splitext(filename)
        name = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, name)


class UniqueImageField(ImageField):
    def generate_filename(self, instance, filename):
        _name, ext = os.path.splitext(filename)
        name = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, name)


class Base(models.Model):
    created_at = models.DateTimeField(_(u'Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_(u'Updated at'), auto_now=True, editable=False)

    class Meta:
        abstract = True

    @property
    def secure_id(self):
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=32)
        return hashids.encrypt(self.id)

    @staticmethod
    def reverse_secure_id(key, default=None):
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=32)
        try:
            return hashids.decode(key)[0]
        except:
            return default


class BaseWithUser(Base):
    user = models.ForeignKey(User, validators=_(u'User'), blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

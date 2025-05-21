# -*- coding: utf-8 -*-
__author__ = 'Vadim'

import os
import json
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from taggit_autosuggest.managers import TaggableManager
from hashids import Hashids
from vu.abstract.models import UniqueFileField

from vu.abstract.models import Base

import logging
log = logging.getLogger(__name__)

__all__ = ['Pygment', 'Share', 'File']

SHARE_UPLOADED_DIR = settings.VCMS_SHARE_UPLOADED_DIR
SHARE_PROTECTED_DIR = settings.VCMS_SHARE_PROTECTED_DIR


def default_json():
    return {}

class Pygment(models.Model):
    name = models.CharField(_(u'Name'), max_length=32)
    code = models.CharField(_(u'Code'), max_length=16)
    enabled = models.BooleanField(_(u'Enabled'), default=True)

    class Meta:
        verbose_name = _(u'Pygment type')
        verbose_name_plural = _(u'Pygment types')

    def __str__(self):
        return self.name


class Share(Base):

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    tags = TaggableManager(_(u'Tags'), blank=True)
    type = models.ForeignKey(Pygment, verbose_name=_(u'Pygment type'), blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_(u'Title'),max_length=255, blank=True, null=True)
    slug = models.SlugField(_(u'Slug'),max_length=255, blank=True, null=True, db_index=True)
    url = models.CharField(_(u'Url'),max_length=255, blank=True, null=True)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    content = models.TextField(_(u'Content'), blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, db_index=True)
    disabled = models.BooleanField(default=False, db_index=True)
    hidden = models.BooleanField(default=False, db_index=True)
    personal = models.BooleanField(_(u'Personal'), default=False)
    json = models.JSONField(_(u'Json content'), default=default_json)

    expired_on = models.DateField(_(u'Expired on'), blank=True, null=True)
    view_count = models.IntegerField(default=0, editable=False)
    time_delete = models.DateField(default=None, blank=True, null=True)

    # def rm_files(self):
    #     try:
    #         if self.thumbnail and self.pk:
    #             log.debug("Request to delete thumbnail: %s" % self.thumbnail)
    #             os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail))
    #         if self.file and self.pk:
    #             log.debug("Request to delete file: %s" % self.file.name)
    #             os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
    #     except Exception as e:
    #         log.error('Cannot remove files for share with id: %s. Error: %s' % (self.pk, e))

    def save(self, *args, **kwargs):
        # if self.description is not None:
        #     self.description_html = markdown(self.description, extensions=['codehilite'])
        #
        # if not self.pk:
        #     expl = self.title.split('/')
        #     if len(expl) > 1:
        #         self.title = expl[0]
        #         self.slug = self.unique_slug(slugify(expl[1]))
        #
        # if not self.title and self.file_name:
        #     if self.file_type == 'image':
        #         file_type = 'Picture'
        #     else:
        #         file_type = 'File'
        #     self.title = _(u'%s: %s' % (file_type, self.file_name))
        # elif not self.title and self.url:
        #     self.title = _(u'Url to: %s %s' % (self.url[:32], '...' if len(self.url) > 32 else ''))
        #
        # self.type = self.file_type()
        # self.get_title()

        super(Share, self).save()

        if self.slug is None:
            self.slug = self.short_id
            super(Share, self).save()

    # def process_file(self):
    #     filename, file_extension = os.path.splitext(self.file)
    #     file_name = "%s%s" % (slugify(filename), file_extension)

    @property
    def download_url(self):
        return reverse('share:download_file', args=[self.short_id])

    @property
    def base_url(self):
        return reverse('share:snippet', args=[self.short_id])

    @property
    def redirect_url(self):
        return reverse('share:link_redirect', args=[self.short_id])

    @property
    def view(self):
        if self.url and self.video_link is False:
            return self.redirect_url
        else:
            return self.base_url

    @property
    def allow_change(self):
        if self.user:
            return True
        else:
            return False

    def unique_slug(self, slug, counter=0):
        if counter > 0:
            unique_slug = "%s%s" % (slug, counter)
        else:
            unique_slug = slug

        if self.id:
            my_id = self.id
        else:
            my_id = 0

        if Share.objects.filter(slug=unique_slug).exclude(id=my_id).exists():
            counter += 1
            return self.unique_slug(slug, counter)
        else:
            return unique_slug

    @property
    def short_id(self):
        if self.slug:
            return self.slug
        else:
            hashids = Hashids(salt=settings.SECRET_KEY, min_length=4)
            return hashids.encrypt(self.id)

    def get_absolute_url(self):
        return '/%s/%s' % ('share', self.short_id)

    # def file_type(self):
    #     if self.file_name is not None:
    #         filename, file_extension = os.path.splitext(self.file_name)
    #         if file_extension.lower() in ['.jpg', '.jpeg', '.gif', '.png']:
    #             return 'image'
    #         else:
    #             return 'file'
    #     return self.type

    # @property
    # def video_link(self):
    #     if self.url:
    #         try:
    #             match = detect_backend(self.url)
    #             print(match)
    #             if match:
    #                 return True
    #         except:
    #             pass
    #     return False

    def __str__(self):
        return self.title


class File(Base):
    TYPE_IMAGE = 'image'

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    share = models.ForeignKey(Share, blank=True, null=True, related_name='file_share', on_delete=models.CASCADE)
    file = UniqueFileField(_(u'File'), upload_to='share/%Y/%m/%d')
    name = models.CharField(_(u'Name'), max_length=255)
    mime = models.CharField(max_length=128, blank=True, null=True)
    json = models.JSONField(_(u'Json content'), default=default_json)
    processed = models.BooleanField(_(u'Processed'), default=False)
    comment = models.TextField(_(u'Comments'), blank=True, null=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    @property
    def is_private(self):
        if hasattr(self, '__private'):
            return self.__private
        else:
            log.debug(f'Check file {self} for public access')
            self.__private = self.share.personal
        return self.__private

    def download(self):
        if self.is_private is False:
            return self.file.url
        else:
            return '/no-download/'



# @receiver(models.signals.pre_save, sender=Share)
# def share_on_change(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             obj = Share.objects.get(pk=instance.pk)
#             if instance.file and instance.file != obj.file:
#                 print(instance.file)
#                 print(obj.file)
#                 log.debug('Deleting old files')
#                 obj.rm_files()
#         except Exception as e:
#             log.error(e)



    # instance.rm_files()

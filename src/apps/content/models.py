# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
from uuid import uuid4

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from taggit.models import Tag, TaggedItem
from taggit_autosuggest.managers import TaggableManager
from treebeard.al_tree import AL_Node

from vu.abstract.models import unique_slug
from vu.abstract.models import Base

if hasattr(settings, 'VCMS_POST_CUTTER'):
    cutter = settings.VCMS_POST_CUTTER
else:
    cutter = '<!-- cut -->'


def default_json():
    return {}


class PostTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
            slug = slugify(tag.lower())
            if i is not None:
                slug += '-%d' % i
            return slug


class PostTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return PostTag


def get_upload_path(instance, filename):
    return instance.get_upload_path(filename)


class Content(AL_Node, Base):
    HASH_LENGTH = 8
    TYPE_HTML = 'html'
    TYPE_MD = 'md'
    TYPE_PLAIN = 'plain'

    type_choices = (
        (TYPE_HTML, _(u'HTML')),
        (TYPE_MD, _(u'Markdown')),
        (TYPE_PLAIN, _(u'Plain text')),
    )

    # adjacency list settings
    uuid = models.UUIDField(_(u'UUID'), default=uuid4, editable=False, unique=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_(u'Parent content'), db_index=True)
    sib_order = models.PositiveIntegerField(_(u'Sibling order'), default=0)

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_user')
    tags = TaggableManager(_(u'Tags'), through=PostTaggedItem, blank=True, related_name='content_tags')

    # Fields
    title = models.CharField(_(u'Title'), max_length=255, default='')
    url = models.CharField(_(u'Path'), max_length=255, default='', editable=False, db_index=True)
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255, db_index=True)
    template = models.CharField(_(u'Template'), choices=settings.VCMS_TEMPLATES, max_length=100, default='content_view')
    language = models.CharField(_(u'Language'), choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE,
                                max_length=5)
    type = models.CharField(max_length=64, choices=type_choices, db_index=True, default=TYPE_HTML)
    date_published = models.DateField(_(u'Date published'), default=timezone.now, db_index=True)
    content = models.TextField(_(u'Content'), blank=True)

    # Access settings
    allow_comments = models.BooleanField(_(u'Allow comments'), default=False)
    is_enabled = models.BooleanField(_(u'Enabled'), default=True, db_index=True)
    is_hidden = models.BooleanField(_(u'Is hidden'), default=False, db_index=True)
    pass_access = models.CharField(_(u'Password'), max_length=64, blank=True, null=True)

    json = models.JSONField(_(u'Json content'), default=dict, editable=False)

    node_order_by = ['date_published']

    class Meta:
        verbose_name = _(u'Content')
        verbose_name_plural = _(u'Content')

    def __str__(self):
        return self.title

    @property
    def short_content(self):
        result = re.findall(r"(?si)<p>(.*?)<\/p>", self.content)
        try:
            return result[0]
        except Exception as e:
            # print(re.sub('<[^<]+?>', '', self.content))
            return ''

    @property
    def long_content(self):
        return self.content

    def update_url(self):
        url = self.slug
        parent = self.get_parent(update=True)
        if parent:
            url = "%s/%s" % (parent.url, self.slug)

        if self.url != url:
            Content.objects.filter(id=self.pk).update(url=url)

            children = self.get_children()
            for child in children:
                child.update_url()

    def save(self, *args, **kwargs):
        update_slug = False
        if self.pk is not None:
            old = Content.objects.get(pk=self.pk)
            if old.slug != self.slug:
                update_slug = True
        else:
            update_slug = True

        if update_slug is True:
            self.slug = unique_slug(
                Content, 'slug', self.slug, query={'type': self.type}
            )

        super(Content, self).save(*args, **kwargs)
        if update_slug is True:
            self.update_url()

    def reverse(self):
        if self.language == settings.LANGUAGE_CODE:
            prefix = ''
        else:
            prefix = '/%s' % self.language
        return prefix + reverse('content_page', args=[self.url])


class Files(Base):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(_(u'File'), upload_to='content/%Y/%m/%d')
    title = models.CharField(_(u'Title'), max_length=255, default='', blank=True)
    description = models.TextField(_(u'Description'), blank=True)

    class Meta:
        verbose_name = _(u'File')
        verbose_name_plural = _(u'Files')

    def __str__(self):
        return self.title or self.file.name



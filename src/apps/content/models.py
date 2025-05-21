# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from datetime import datetime
import re

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.models import Tag, TaggedItem
from taggit_autosuggest.managers import TaggableManager
from treebeard.mp_tree import MP_Node

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


class Category(Base):
    name = models.CharField(_(u'Name'), max_length=100, default='')
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=100)
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255, default='', blank=True)
    meta_description = models.CharField(_(u'Meta description'), max_length=255, default='', blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True)
    hidden = models.BooleanField(_(u'Is hidden'), default=False)

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Content(MP_Node, Base):
    HASH_LENGTH = 8
    TYPE_PAGE = 'page'
    TYPE_GALLERY = 'gallery'
    type_choices = (
        (TYPE_PAGE, _(u'Page')),
        (TYPE_GALLERY, _(u'Gallery')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_user')
    tags = TaggableManager(_(u'Tags'), through=PostTaggedItem, blank=True, related_name='content_tags')
    title = models.CharField(_(u'Title'), max_length=255, default='')
    url = models.CharField(_(u'Path'), max_length=255, default='', editable=False, db_index=True)
    slug = models.SlugField(verbose_name=_(u'Slug'), max_length=255, db_index=True)
    template = models.CharField(_(u'Template'), choices=settings.VCMS_TEMPLATES, max_length=100, default='content_view')
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255, default='', blank=True)
    meta_description = models.CharField(_(u'Meta description'), max_length=255, default='', blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True, db_index=True)
    hidden = models.BooleanField(_(u'Is hidden'), default=False, db_index=True)
    category = models.ManyToManyField(Category, verbose_name=_(u'Category'), blank=True)
    type = models.CharField(max_length=64, choices=type_choices, db_index=True, default=TYPE_PAGE)
    image = models.ImageField(upload_to='content/%Y/%m/%d', blank=True)
    date_published = models.DateField(_(u'Date published'), default=timezone.now, db_index=True)
    content = RichTextUploadingField(_(u'Content'), blank=True)
    # content = RichTextField(_(u'Content'), blank=True)
    comments = models.BooleanField(_(u'Allow comments'), default=False)
    language = models.CharField(_(u'Language'), choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, max_length=5)

    json = models.JSONField(_(u'Json content'), default=default_json, editable=False)
    rating = models.IntegerField(_(u'Rating'), default=0)
    show_count = models.IntegerField(_(u'Show count'), default=0)
    view_count = models.IntegerField(_(u'View count'), default=0)

    node_order_by = ['date_published']

    class Meta:
        verbose_name = _(u'Content')
        verbose_name_plural = _(u'Content')

    def __str__(self):
        return self.title

    def allow_comment(self):
        return self.comments

    @property
    def parent(self):
        return 1

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

    def get_upload_path(self, filename):
        return 'content/%s/%s' % (datetime.now().strftime("%Y/%m"), filename)

    def __unique_slug(self, slug, my_id, counter=1):
        counter += 1
        gen_slug = "%s-%s" % (slug, counter)
        exists = self._default_manager.filter(slug=gen_slug).exclude(id=my_id)
        if exists:
            return self.__unique_slug(slug, my_id, counter)
        else:
            return gen_slug

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
                # Content, 'slug', self.slug, query={'parent': self.parent, 'type': self.type}
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

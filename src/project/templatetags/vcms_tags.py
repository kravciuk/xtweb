# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
import time
from django.conf import settings
from django import template
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, get_language
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from content.models import Content

register = template.Library()

from logging import getLogger
log = getLogger(__name__)


@register.simple_tag(takes_context=True)
def content_root_tree(context, show_hidden=False):
    rs = Content.objects.filter(is_enabled=True, depth=1, language=get_language()).order_by('path')
    if show_hidden is False:
        rs = rs.filter(is_hidden=False)
    return rs


@register.simple_tag(takes_context=True)
def content_annotate_list(context, show_hidden=False):
    rs = Content.get_annotated_list()
    if show_hidden is False:
        rs = rs.filter(is_hidden=False)
    return rs


@register.filter(name='addclass')
def addclass(field, my_class):
   return field.as_widget(attrs={"class":my_class})


@register.simple_tag(takes_context=True)
def content_edit_link(context, obj):
    res = ''
    if context['request'].user.is_authenticated():
        if context['request'].user.is_superuser or obj.user == context['request'].user:
            res = '<a href="%s?page=%s">%s</a>' % (
                reverse('content_edit', args=[obj.type]),
                obj.hash,
                _(u'Edit content')
            )
    return mark_safe(res)





@register.simple_tag
def vcms_page(*args, **kwargs):
    url = kwargs.get('url')
    try:
        return Content.objects.filter(is_enabled=True, url=url).get()
    except Exception as e:
        log.error('Cannot get page by url: %s'% url)
        return None


@register.simple_tag(takes_context=True)
def vcms_pages(context, *args, **kwargs):
    parent = kwargs.get('parent')
    language = kwargs.get('lang')
    limit = kwargs.get('limit', 10)
    page = context['request'].GET.get('page', 1)

    log.debug(context['request'].user.is_authenticated)
    user_id = context['request'].user.id if context['request'].user.is_authenticated is True else 0
    rs = Content.objects.filter(Q(is_published=True, is_hidden=False)|Q(user_id=user_id))
    if parent:
        try:
            rs = rs.filter(url=parent).get().get_children()
        except:
            return []

    if language:
        rs = rs.filter(language=language)

    rs = rs.order_by('-date_published', '-id')
    paginator = Paginator(rs, limit)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result


# @register.simple_tag()
# def last_snippets(snippet_type='source', limit=20, show_hidden=False):
#     res = Share.objects.filter(type=snippet_type, password='', disabled=False, personal=False)
#     if show_hidden is False:
#         res = res.filter(hidden=False)
#     res = res.order_by('-pk')[:limit]
#
#     return {
#         'records': res
#     }


@register.simple_tag(takes_context=True)
def share_download_url(context, obj):
    remote_addr = context['request'].META['REMOTE_ADDR']
    timestamp = int(time.time())
    encrypted_key = encrypt(settings.SECRET_KEY, "%s %s" % (timestamp, remote_addr))
    return reverse('share:download', args=[obj.short_id, encrypted_key])


@register.simple_tag
def content_url(obj):
    if obj.type == 'gallery':
        return reverse('content_gallery', args=[obj.path])
    else:
        return reverse('content_page', args=[obj.url])


@register.simple_tag(takes_context=True)
def web_path(context, scheme='auto'):
    if scheme == 'auto':
        scheme = context['request'].scheme
    return "%s://%s" % (scheme, context['request'].get_host())



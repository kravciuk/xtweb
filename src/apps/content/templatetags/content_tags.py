# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import logging
from django import template


log = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('content/js_admin_layer.html', takes_context=True)
def js_admin_layer(context):
    current_page_hash = None
    if 'content' in context:
        if hasattr(context['content'], 'url'):
            current_page_hash = context['content'].hash

    if context['request'].user.is_superuser is True:
        return {
            'menu': True,
            'current_page_hash': current_page_hash,
        }
    else:
        return {'menu': False}

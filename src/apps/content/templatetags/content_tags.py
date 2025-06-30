# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import logging
from django import template


log = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('content/js_admin_layer.html', takes_context=True)
def js_admin_layer(context):
    result = {'menu': False}
    if context['request'].user.is_superuser is True:
        result['menu'] = True

        if 'content' in context:
            result['content_uuid'] = context['content'].uuid
            result['content_type'] = context['content'].type

    return result

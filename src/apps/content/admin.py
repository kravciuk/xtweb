# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Content


class ContentAdmin(TreeAdmin):
    form = movenodeform_factory(Content)
    list_display = ('title', 'is_hidden', 'type', 'slug')
    list_filter = ['is_hidden', 'type', 'type']
    prepopulated_fields = {'slug': ('title',)}


    def get_form(self, request, obj=None, **kwargs):
        form = super(ContentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['slug'].widget.attrs['style'] = 'width: 50%;'
        form.base_fields['title'].widget.attrs['style'] = 'width: 50%;'
        form.base_fields['tags'].widget.attrs['style'] = 'width: 50%;'
        return form

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'user') is False:
            obj.user = request.user
        obj.save()


admin.site.register(Content, ContentAdmin)

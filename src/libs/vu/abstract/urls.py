# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views


app_name = 'example'
urlpatterns = [
    url(r'^task/$', views.view_task, name='task')
]

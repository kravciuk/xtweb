# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.urls import path, re_path
from .views import *

app_name = 'content'
urlpatterns = [
    # re_path(r'^index/(?P<content_type>[a-z]+)/$', index, name='index'),
    path('edit/<slug:content_type>/', add_or_edit, name='edit'),
    # path('<slug:slug>/', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page'),
    # re_path(r'^post-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'news'}, name='news'),
    # re_path(r'^gallery-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'gallery'}, name='gallery'),
    # re_path(r'^$', content_view, kwargs={'content_type': 'page'}, name='page_index'),
    re_path(r'^$', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page_index'),
    path('<slug:slug>/', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page'),
]

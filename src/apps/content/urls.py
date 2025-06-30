# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.urls import path, re_path
from .views import *

app_name = 'content'
urlpatterns = [
    # re_path(r'^index/(?P<content_type>[a-z]+)/$', index, name='index'),
    path('edit/<slug:type>/<slug:uuid>/', PageContentUpdateView.as_view(), name='edit'),
    path('add/<slug:type>/', PageContentCreateView.as_view(), name='add'),
    # path('<slug:slug>/', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page'),
    # re_path(r'^post-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'news'}, name='news'),
    # re_path(r'^gallery-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'gallery'}, name='gallery'),
    # re_path(r'^$', content_view, kwargs={'content_type': 'page'}, name='page_index'),
    re_path(r'^$', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page_index'),
    path('<path:slug>/', ContentView.as_view(), kwargs={'content_type': 'page'}, name='page'),
]

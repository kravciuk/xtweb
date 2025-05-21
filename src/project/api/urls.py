# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf import settings
from django.urls import path, re_path, include
from rest_framework.authtoken import views as RestViews

urlpatterns = [
    path('v1/api-token-auth/', RestViews.obtain_auth_token),
]

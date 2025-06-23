# -*- coding: utf-8 -*-
import os
import sys
import importlib
import re

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
VAR_DIR = os.path.normpath(os.path.join(BASE_DIR, '../var'))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'libs'))
SECRET_KEY = '=75dq8^7#rj%s#d#n^!9uer=s0hfvyd+d&knbn!2q5y2y28uh6'

SITE_ID = 1
DEBUG = False

ALLOWED_HOSTS = ['localhost']
ALLOWED_IPS = ['127.0.0.1', '192.168/16']

INSTALLED_APPS = (
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'compressor',
    # 'dbbackup',
    'crispy_forms',
    'sekizai',
    'widget_tweaks',
    #'adminsortable2',
    'constance',
    'constance.backends.database',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'taggit_autosuggest',
    'treebeard',
    'sitetree',
    'django_ckeditor_5',
    # 'ckeditor_uploader',
    'django_celery_results',
    'django_celery_beat',

    # 'vu',
    # 'vu.sendfile',


    'content',
    # 'share',
    # 'comments',
    'project',

)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = os.path.join(VAR_DIR, 'htdocs/static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(VAR_DIR, 'htdocs/media')
MEDIA_URL = '/media/'

ADMIN_LOCATION_URL = 'admin'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

ASGI_APPLICATION = "project.asgi.application"

# create var dir
if os.path.exists(VAR_DIR) is False:
    print("Creating var directory at %s" % VAR_DIR)
    os.makedirs(VAR_DIR+'/htdocs')
    os.makedirs(VAR_DIR+'/htdocs/static')
    os.makedirs(VAR_DIR+'/htdocs/media')
    os.makedirs(VAR_DIR+'/logs')
    os.makedirs(VAR_DIR+'/protected')
    os.makedirs(VAR_DIR+'/backup')


# load base settings
from .logging import *
from .database import *
from .celery import *
from .regional import *
from .additional import *
from .constance import *
from .templates import *
from .vcms import *

LOCAL_MIDDLEWARE = ()
LOCAL_APPS = ()

# load local settings
rs = os.listdir(os.path.join(BASE_DIR, 'project/settings/local'))

for file_name in rs:
    match = re.search(r"(.*).py$", file_name, re.MULTILINE)
    if match:
        globals().update(importlib.import_module('project.settings.local.%s'%file_name[:-3]).__dict__)

MIDDLEWARE += LOCAL_MIDDLEWARE
INSTALLED_APPS += LOCAL_APPS


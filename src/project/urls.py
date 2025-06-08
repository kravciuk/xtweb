# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic import TemplateView
from django.contrib import admin

from sitetree.sitetreeapp import register_i18n_trees

from .sitemaps import ProjectSitemap
from . import views

handler404 = 'project.views.error404'

register_i18n_trees(['header_menu'])

sitemaps = {
    'general': ProjectSitemap(),
}

urlpatterns = [
    re_path(r'^%s/' % settings.ADMIN_LOCATION_URL, admin.site.urls),

    re_path(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}),
    re_path(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}),
    re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^select2/', include('django_select2.urls')),
    path('api/', include('project.api.urls')),
]

if 'silk' in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns += i18n_patterns(
    re_path(r'^$',TemplateView.as_view(template_name='index.html'), name="index"),
    path('healthcheck/',TemplateView.as_view(template_name='healthcheck.html'), name="healthcheck"),
    path('self/', TemplateView.as_view(template_name='local.html'), name="local"),
    re_path(r'^sitemap-content/$',TemplateView.as_view(template_name='sitemap.html'), name="sitemap_content_html"),

    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^share/', include('share.urls')),

     # path('example/', include('example.urls', namespace='example')),
     path('', include('content.urls')),

    prefix_default_language=settings.PREFIX_DEFAULT_LANGUAGE
)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()


websocket_urlpatterns = [
    # path("ws/game/", consumers.MultiplayerConsumer.as_asgi()),
]

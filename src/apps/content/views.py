# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

__all__ = [
    'IndexPage',
    'index',
    'PageContentCreateView',
    'PageContentUpdateView',
    'ContentView',
]

import re
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.views import View
from django.http import HttpResponseNotFound
from django.shortcuts import render

from vu.paginator import FlynsarmyPaginator
from vu.abstract.views.class_based import PageView

from .forms import PageContentForm
from .models import Content
from .tasks import rehost_content

import logging
log = logging.getLogger(__name__)


class IndexPage(PageView):
    pk_url_kwarg = 'slug'


def index(request, content_type="page"):
    full_listing = Content.objects.filter(type=content_type).filter(Q(is_published=True, is_hidden=False)|Q(user=request.user))

    paginator = FlynsarmyPaginator(full_listing.order_by('-id'), 30, adjacent_pages=20)
    page = request.GET.get('page')

    try:
        listing = paginator.page(page)
    except PageNotAnInteger:
        listing = paginator.page(1)
    except EmptyPage:
        listing = paginator.page(paginator.num_pages)

    content = []
    return render(request, 'content/index.html', {
        'content': content,
        'listing': listing,
        'host': request.META['HTTP_HOST'],
        'content_type': content_type,
    })


class PageContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    form_class = PageContentForm
    template_name = 'content/page_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['after'] = self.request.GET.get('after', self.request.POST.get('after'))
        # initial['type'] = self.kwargs.get('type', 'html')
        return initial

    def form_valid(self, form):
        after = form.cleaned_data.get('after')

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.language = self.request.LANGUAGE_CODE


        if after:
            node = get_object_or_404(Content, uuid=after, user=self.request.user)
            self.object = node.add_child(instance=self.object)
        else:
            self.object = Content.add_root(instance=self.object)

        if hasattr(form, 'save_m2m'):
            # Save many-to-many relationships if the form has them
            # This is necessary for tags or other m2m fields
            form.save_m2m()

        if form.cleaned_data.get('rehost'):
            rehost_content(self.object.pk)

        messages.add_message(self.request, messages.INFO, _(u'Record saved.'))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('content:edit', args=[self.object.type, self.object.uuid])

    def form_invalid(self, form):
        log.debug(f"Form invalid: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))


class PageContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = PageContentForm
    template_name = 'content/page_form.html'
    pk_url_kwarg = 'page'
    slug_field = 'uuid'
    slug_url_kwarg = 'page'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Content, uuid=self.kwargs.get('uuid'), user=self.request.user)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete_button' in request.POST:
            try:
                ins_type = self.object.type
                self.object.delete()
                messages.add_message(request, messages.INFO, _(u'Record deleted.'))
                return redirect(reverse('content_index', args=[ins_type]))
            except Exception as e:
                messages.add_message(request, messages.ERROR, f"{_(u'Failed to delete record.')} {e}")
                log.debug(f"Error deleting record: {e}")
                return self.render_to_response(self.get_context_data(form=self.get_form()))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        super().form_valid(form)
        if form.cleaned_data.get('rehost'):
            rehost_content(self.object.pk)
        messages.add_message(self.request, messages.INFO, _(u'Record saved.'))
        return redirect(self.get_success_url())


    def get_success_url(self):
        return reverse('content:edit', args=[self.object.type, self.object.uuid])


class ContentView(View):
    def get(self, request, slug='index', *args, **kwargs):
        search_rules = {}
        log.debug(f'Slug: {slug}')
        uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        if re.match(uuid_regex, slug):
            search_rules['uuid'] = slug
        else:
            search_rules['url'] = slug

        obj = Content.objects.filter(language=request.LANGUAGE_CODE).filter(**search_rules).first()
        if obj:
            return render(request, f"content/{obj.template}.html", {
                'content': obj,
            })
        else:
            return HttpResponseNotFound(f'Page /{slug}/ not found.')

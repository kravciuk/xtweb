# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

__all__ = ['Create', 'Edit', 'PageView']

from logging import getLogger

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, DeleteView, ListView


log = getLogger(__name__)


class Create(CreateView):
    template_name = 'example/create.html'
    form_class = None
    model = None
    success_url = reverse_lazy('example')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        log.debug(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        messages.add_message(
            self.request, messages.SUCCESS, _(u'Record saved'))
        return redirect(reverse_lazy('example', args=[obj.id]))


class Edit(UpdateView):
    template_name = 'example/create.html'
    form_class = None
    model = None
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('example')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        log.debug(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        obj = form.save()
        obj.save()

        messages.add_message(
            self.request, messages.SUCCESS, _(u'Record saved'))
        return redirect(self.success_url)


class PageView(DetailView):
    template_name = 'example/page-view.html'
    model = None
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Sample(TemplateView):
    template_name = 'example/create.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

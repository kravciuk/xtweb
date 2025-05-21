# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from logging import getLogger

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Q, Subquery

from django_filters.views import FilterView
from django_filters import FilterSet, CharFilter, filters
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView, Table, Column, CheckBoxColumn

log = getLogger(__name__)


def tags_filter(request):
    if request is None:
        return Tag.objects.none()

    return Tag.objects.filter(user=request.user, apps='location').all().order_by('label')


class ExampleTable(Table):
    name = Column(
        empty_values=(),
        verbose_name = _(u'Managers'),
        orderable=False,
        attrs={
            "td": {"class": "text-primary"}
        },
    )

    def render_name(self, value, record):
        return format_html(record.name)

    class Meta:
        model = None
        template_name = "example/custom-table.html"
        fields = ['name']
        attrs = {"class": "table table-striped table-hover locations-table"}
        row_attrs = {

        }


class ExampleFilter(FilterSet):
    name = CharFilter(method='string_search', label='Search string')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=tags_filter, label=_(u'Tags'), method='filter_tags')
    date_start = CharFilter(method='find_by_date_start')

    class Meta:
        model = None
        fields = ['name', 'tags']

    def string_search(self, queryset, name, value):
        return queryset.filter(Q(address__icontains=value)
                               | Q(name__icontains=value)
                               | Q(company__icontains=value)
                               | Q(zip__icontains=value)
                               | Q(email__icontains=value)
                               | Q(phone__icontains=value)
                               )


    def filter_tags(self, queryset, name, value):
        if value:
            rs = TagObjects.objects.filter(tag__in=value).values('obj_id')
            queryset = queryset.filter(id__in=rs)
        return queryset

    def find_by_date_start(self, queryset, name, value):
        if value:
            queryset = queryset.filter(date_start__gte=value)
        return queryset


class ExampleView(SingleTableMixin, FilterView):
    template_name = 'location/location_list.html'
    model = None
    table_class = ExampleTable
    filterset_class = ExampleFilter
    ordering = ['name']
    table_pagination = {
        "per_page": 10
    }
    vpath = 'locations'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        return qs

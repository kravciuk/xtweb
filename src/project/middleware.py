# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk'
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
import iptools
import logging


def get_ip(request):
    remote_addr = request.META['REMOTE_ADDR']
    if 'HTTP_X_REAL_IP' in request.META:
        remote_addr = request.META['HTTP_X_REAL_IP']

    ip = [remote_addr]
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for and x_forwarded_for not in ip:
        ips = x_forwarded_for.split(',')
        for i in ips:
            ip.append(i)

    return ip


class HostCheck():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hostname = request.get_host()
        if hostname not in settings.ALLOWED_HOSTS:
            remote_addr = get_ip(request)
            logging.error('Access denied by hostname [%s] for ip %s.' % (hostname, (', '.join(remote_addr))))
            return HttpResponseForbidden()

        response = self.get_response(request)
        return response


class IPCheck(object):
    def process_request(self, request):
        allowed_ips = iptools.IpRangeList(*settings.ALLOWED_IPS)

        remote_addr = get_ip(request)
        if not frozenset(remote_addr).intersection(allowed_ips):
            logging.error('Access denied by ip address [%s].' % ', '.join(remote_addr))
            raise PermissionDenied()

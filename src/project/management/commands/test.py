# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'


from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        from django.core.management import execute_from_command_line
        argv = ['', 'dbbackup', '--compress', '--clean']
        execute_from_command_line(argv)
        # c = Command()
        # c.handle({'clean': True, 'compress': True, })

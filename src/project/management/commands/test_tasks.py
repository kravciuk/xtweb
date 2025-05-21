# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.test_image_processor()


    def test_image_processor(self):
        from vcms.share.tasks import task_share_process_file
        task_share_process_file(4)

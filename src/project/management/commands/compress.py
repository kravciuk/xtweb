# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk'

import os
import gzip
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.ext = ['.js', '.css']
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        path = settings.STATIC_ROOT
        for dir_name, sub_dir_list, file_list in os.walk(path):
            for file_name in file_list:
                _name, _ext = os.path.splitext(file_name)
                if _ext in self.ext:
                    print ("%s/%s" % (dir_name, file_name))

                    in_file = "%s/%s" % (dir_name, file_name)
                    out_gz = "%s/%s.gz" % (dir_name, file_name)
                    in_data = open(in_file, "rb").read()
                    gzf = gzip.open(out_gz, "wb")
                    gzf.write(in_data)
                    gzf.close()

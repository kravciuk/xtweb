# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from django.conf import settings
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage

from urllib.parse import urljoin

import logging
log = logging.getLogger(__name__)


class ContentStorage(FileSystemStorage):
    dir_path = [now().year.__str__(), f"{now().month:02d}", f"{now().day:02d}"]
    location = os.path.join(settings.MEDIA_ROOT, "content", *dir_path)
    base_url = urljoin(settings.MEDIA_URL, f"content/{'/'.join(dir_path)}/")

    log.debug(f"ContentStorage initialized with location: {location}, base_url: {base_url}")
    log.debug('/'.join(dir_path))

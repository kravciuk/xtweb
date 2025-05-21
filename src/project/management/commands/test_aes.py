# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import base64
from Crypto import Random
from Crypto.Util.Padding import pad
from Crypto.Cipher import DES, AES
import hashlib
from django.conf import settings

from django.core.management.base import BaseCommand

class AESCipher:
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.urlsafe_b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return bytes(s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs), 'utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        string = '123 test string'
        aes = AESCipher(settings.SECRET_KEY[:16])

        enc = aes.encrypt(string)
        print(enc)
        print(aes.decrypt(enc))



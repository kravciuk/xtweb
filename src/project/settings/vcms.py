# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from django.utils.translation import gettext_lazy as _

from . import MEDIA_ROOT


VCMS_SHARE_UPLOADED_DIR = 'share'
VCMS_SHARE_PROTECTED_DIR = 'restricted'
VCMS_SHARE_THUMBNAIL_WEIGHT = 320
VCMS_SHARE_THUMBNAIL_HEIGHT = 320
VCMS_DOWNLOAD_TIME_LIMIT = 3600*2
VCMS_POST_CUTTER = '<div style="page-break-after: always"><span style="display:none">&nbsp;</span></div>'

VCMS_TEMPLATES = (
    ('content_view', _(u'View single page')),
    ('content_list', _(u'List pages')),
)

# Configure CKEDITOR
# -----------------------------------------------------------------------------------
CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'staff'
CKEDITOR_5_CONFIGS = {
  'default': {
      'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                  'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
      'language': 'de',
  },
}

# CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_BACKEND = 'pillow'
# CKEDITOR_CONFIGS = {
#     'default': {
#         # 'stylesSet': 'my_styles:/static/ckeditor/styles.js',
#         'extraPlugins': 'dialogui,dialog,about,a11yhelp,basicstyles,blockquote,clipboard,panel,floatpanel,menu,'
#                         'contextmenu,resize,button,toolbar,elementspath,enterkey,entities,popup,filebrowser,'
#                         'floatingspace,listblock,richcombo,format,horizontalrule,htmlwriter,wysiwygarea,image,'
#                         'indent,indentlist,fakeobjects,link,list,magicline,maximize,pastetext,pastefromword,'
#                         'removeformat,showborders,sourcearea,specialchar,menubutton,scayt,stylescombo,tab,table,'
#                         'tabletools,undo,wsc,lineutils,widget,notification,notificationaggregator,embedbase,'
#                         'embed,filetools,codesnippet,prism',
#         'toolbar': 'Full',
#         'height': 300,
#         'width': '100%',
#         'toolbar_Full': [
#         ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat' ],
#         ['Image', 'Table', 'HorizontalRule', 'PageBreak', 'CodeSnippet'],
#         ['TextColor', 'BGColor'],
#         ['Link', 'Unlink', 'Embed'],
#         ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
#         ['Source', '-''NewPage', 'Preview', 'Templates', 'PasteText'],
#         ['Maximize', 'ShowBlocks'],
#     ],
#     },
# }

SENDFILE_BACKEND = 'vu.sendfile.backends.nginx'
SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'share')
SENDFILE_URL = '/media/share'

EMBED_VIDEO_BACKENDS = (
    'embed_video.backends.YoutubeBackend',
    'embed_video.backends.VimeoBackend',
    'embed_video.backends.SoundCloudBackend',
    'vcms.video.backends.RedTube',
    'vcms.video.backends.XTube',
)

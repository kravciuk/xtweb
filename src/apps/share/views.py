# -*- coding: utf-8 -*-
__author__ = 'Vadim'

import os
import re
from datetime import datetime
from time import time
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from .forms import AddSnippetForm
from .models import Share, SHARE_PROTECTED_DIR, SHARE_UPLOADED_DIR, File

from vu.paginator import FlynsarmyPaginator

import logging
log = logging.getLogger(__name__)


def download_forbidden(request, short_id):
    content = get_object_or_404(Share, slug=short_id, disabled=False)
    return render(request, 'share/download_forbiden.html', {
        'snippet': content,
    }, status=403)


def link_redirect(request, short_id):
    content = get_object_or_404(Share, slug=short_id, disabled=False)
    if content.url:
        return HttpResponsePermanentRedirect(content.url)
    else:
        return HttpResponseNotFound('Link not found.')


def download_file(request, short_id, enc_key):
    content = get_object_or_404(Share, slug=short_id, disabled=False)

    allow_download = True
    try:
        dec_string = decrypt(settings.SECRET_KEY, enc_key).split(' ')
        expiration_time = dec_string[0]
        allowed_ip = dec_string[1]

        if int(time()) > int(expiration_time) + settings.VCMS_DOWNLOAD_TIME_LIMIT:
            allow_download = False
            log.error("%s for object %s download - time expired." % (request.META['REMOTE_ADDR'], short_id))

        if allowed_ip != request.META['REMOTE_ADDR']:
            allow_download = False
            log.error("%s for object %s download - IP failed, accepted %s." % (request.META['REMOTE_ADDR'], short_id, allowed_ip))
    except Exception as e:
        log.debug(e, exc_info=True)
        allow_download = False
        log.error("%s for object %s download - failed decode string." % (request.META['REMOTE_ADDR'], short_id))

    if content.file and allow_download is True:
        file_path = os.path.join(settings.MEDIA_ROOT, content.file.name)
        return sendfile(
            request,
            file_path,
            attachment=True,
            attachment_filename=content.file_name
        )
    else:
        return redirect('share_download_forbidden', short_id=short_id)


def view_snippet(request, short_id, content_type='html'):
    content = get_object_or_404(Share, slug=short_id, disabled=False)

    # check permission
    if content.personal is True and request.user != content.user:
        return HttpResponseForbidden('Access denied.')

    if content_type == 'raw':
        replace = re.compile(r'(\r\n|\r|\r)')
        return HttpResponse(replace.sub('\n', content.content), content_type='text/plain')
    else:
        return render(request, 'share/snippet.html', {
            'snippet': content,
        })


@login_required
def add_or_edit(request, short_id=''):
    pk = hash_to_id(short_id, default=0, salt=settings.SECRET_KEY)
    log.debug(pk)

    instance = Share.objects.filter(pk=pk, user=request.user).first()
    log.debug(instance)
    if request.method == 'GET':
        form = AddSnippetForm(instance=instance)
    else:
        form = AddSnippetForm(request.POST, request.FILES, instance=instance)

    if instance:
        log.debug("Find file for delete select")
        form.fields['delete_file'].choices = [(x.uuid, x.name) for x in instance.file_share.all()]

    if request.method == 'POST':
        if request.POST.get('delete') and instance is not None:
            instance.delete()
            return redirect('share:personal')

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user

            # format content
            # if instance.content != '' and instance.type:
            #     lexer = get_lexer_by_name(instance.type.code, stripall=True)
            #     formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
            #     instance.content_html = highlight(instance.content, lexer, formatter)
            # else:
            #     instance.content_html = None

                # if instance.pk:
                #     instance.thumbnail = None
                #     instance.rm_files()
                #
                # result = _upload_file(request.FILES['file'], password=instance.password)
                # file_full_path = os.path.join(result.raw_path, result.name)
                # instance.file_name = request.FILES['file'].name[:128]
                # instance.file = os.path.join(result.path, result.name)
                #
                # if instance.file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                #     source = open(file_full_path, 'rb')
                #     try:
                #         th = Thumbnail(source=source)
                #         th_content = th.generate()
                #         fp = open(os.path.join(result.raw_path, 'th_'+result.name), 'wb')
                #         fp.write(th_content.read())
                #         fp.close()
                #         source.close()
                #         th_content.close()
                #         instance.thumbnail = os.path.join(result.path, 'th_'+result.name)
                #     except Exception as e:
                #         log.error("Error creating thumbnail file: %s" % e)

            instance.save()
            form.save_m2m()

            for file in form.cleaned_data.get('delete_file'):
                File.objects.filter(uuid=file, share=instance).delete()

            if request.FILES.get('file'):
                for file_obj in request.FILES.getlist('file'):
                    File.objects.create(
                        user=request.user,
                        share=instance,
                        file=file_obj,
                        mime=file_obj.content_type.split('/')[0],
                        name=file_obj.name,
                    )

            return redirect('share:snippet', short_id=instance.short_id)
        else:
            log.debug("FORM Errors: %s" % form.errors)

    return render(request, 'share/form.html', {
        'form': form,
        'instance': instance,
    })


def _upload_file(file_object, password=None):
    filename, file_extension = os.path.splitext(file_object.name)
    file_name = "%s%s" % (slugify(filename), file_extension)
    upload_path = os.path.join(settings.MEDIA_ROOT, SHARE_UPLOADED_DIR)
    access_path = SHARE_UPLOADED_DIR

    if password != '':
        upload_path = os.path.join(upload_path, SHARE_PROTECTED_DIR)
        access_path = os.path.join(access_path, SHARE_PROTECTED_DIR)

    today = datetime.date(datetime.now())
    upload_path = os.path.join(upload_path, "%s/%s/%s" % (today.strftime("%y"), today.month, today.day))
    access_path = os.path.join(access_path, "%s/%s/%s" % (today.strftime("%y"), today.month, today.day))

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    new_file_name = unique_file_name(upload_path, file_name)
    fp = open('%s/%s' % (upload_path, new_file_name), 'wb')
    for chunk in file_object.chunks():
        fp.write(chunk)
    fp.close()

    result = lambda: result
    result.path = access_path
    result.raw_path = upload_path
    result.name = new_file_name

    return result


@login_required
def share_personal(request):
    return index(request, owner=True)


def index(request, owner=False):
    share_list = Share.objects.filter(hidden=False, disabled=False)
    if owner is True:
        share_list = share_list.filter(user=request.user)
    else:
        share_list = share_list.filter(personal=False)

    paginator = FlynsarmyPaginator(share_list.order_by('-id'), 30, adjacent_pages=20)
    page = request.GET.get('page')

    try:
        shares = paginator.page(page)
    except PageNotAnInteger:
        shares = paginator.page(1)
    except EmptyPage:
        shares = paginator.page(paginator.num_pages)

    content = []
    return render(request, 'share/index.html', {'content': content,
                                                'shares': shares,
                                                'host': request.META['HTTP_HOST']})


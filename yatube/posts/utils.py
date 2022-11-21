from django.core.paginator import Paginator
from django.conf import settings
import os


def make_paginator(request, data):
    paginator = Paginator(data, settings.NUMBER_POSTS_ON_ONE_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def read_file(file):
    if file:
        text_file = []
        path = os.path.join(settings.MEDIA_ROOT, str(file))
        f = open(path, 'r', encoding='utf-8')
        for line in f:
            text_file.append(line)
        return text_file
    return ''

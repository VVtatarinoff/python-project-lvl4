from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _

HEAD_TITLE = 'head_title'


def index(request):
    print(request.LANGUAGE_CODE)
    #title = gettext('Task manager Hexlet')
    title = _(HEAD_TITLE)
    return render(request, 'main.html', {'title': title})

def users(request):
    return HttpResponse('Users')

def login(response):
    return HttpResponse('Login')

def users_create(response):
    return HttpResponse('Create user')

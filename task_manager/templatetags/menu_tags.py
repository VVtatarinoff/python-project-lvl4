from django import template
from django.utils.translation import gettext as _

import statuses.views
import labels.views
import users.views
import tasks.views

register = template.Library()

MAIN_MENU = [{'title': _('Task manager'), 'path': 'home', 'active': 'active'},
             {'title': _('Users'), 'path': users.views.LIST_VIEW},
             {'title': _('Statuses'), 'path': statuses.views.LIST_VIEW},
             {'title': _('Labels'), 'path': labels.views.LIST_VIEW},
             {'title': _('Tasks'), 'path': tasks.views.LIST_VIEW}]

LOGIN_MENU = [{'title': _('Login'), 'path': 'login'},
              {'title': _('Register'), 'path': users.views.CREATE_VIEW}]

LOGGED_MENU = [{'title': _('Logout'), 'path': 'logout'}, ]


@register.simple_tag(name='main_menu')
def get_main_menu(authorized=False):
    if authorized:
        main_menu = MAIN_MENU[:]
    else:
        main_menu = MAIN_MENU[:2]
    return main_menu


@register.simple_tag(name='login_menu')
def get_login_menu(authorized=False):
    if authorized:
        login_menu = LOGGED_MENU[:]
    else:
        login_menu = LOGIN_MENU[:]
    return login_menu

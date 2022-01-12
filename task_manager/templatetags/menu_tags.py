from django import template
from django.utils.translation import gettext as _

from task_manager.views.constants import (LIST_LINKS, USER_CATEGORY,
                                          STATUS_CATEGORY, LABEL_CATEGORY,
                                          TASK_CATEGORY, CREATE_LINKS)

register = template.Library()

MAIN_MENU = [{'title': _('Task manager'), 'path': 'home', 'active': 'active'},
             {'title': _('Users'), 'path': LIST_LINKS[USER_CATEGORY]},
             {'title': _('Statuses'), 'path': LIST_LINKS[STATUS_CATEGORY]},
             {'title': _('Labels'), 'path': LIST_LINKS[LABEL_CATEGORY]},
             {'title': _('Tasks'), 'path': LIST_LINKS[TASK_CATEGORY]}]

LOGIN_MENU = [{'title': _('Login'), 'path': 'login'},
              {'title': _('Register'), 'path': CREATE_LINKS[USER_CATEGORY]}]

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

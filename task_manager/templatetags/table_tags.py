from django import template
from django.utils.translation import gettext as _
from task_manager.models import Status, Label, Task
from django.contrib.auth.models import User

register = template.Library()
STATUS_CATEGORY = 'statuses'
LABEL_CATEGORY = 'labels'
TASK_CATEGORY = 'tasks'
USER_CATEGORY = 'users'

TITLES = {STATUS_CATEGORY: _("Statuses"),
          LABEL_CATEGORY: _("Labels"),
          TASK_CATEGORY: _("Tasks"),
          USER_CATEGORY: _("Users")}

TABLE_HEADS = {STATUS_CATEGORY: ('ID', _('Name'), _('Creation date')),
               LABEL_CATEGORY: ('ID', _('Name'), _('Creation date')),
               TASK_CATEGORY: ('ID', _('Name'), _('Status'), _('Author'), _('Executor'), _('Creation date')),
               USER_CATEGORY: ('ID', _('User name'),
                               _('Full name'), _('Creation date'))}

CREATE_LINKS = {STATUS_CATEGORY: {'name': 'create_status', 'title': _('Create status')},
                LABEL_CATEGORY: {'name': 'create_label', 'title': _('Create label')},
                TASK_CATEGORY: {'name': 'create_task', 'title': _('Create task')},
                USER_CATEGORY: {'name': '', 'title': ''}}

MODELS = {STATUS_CATEGORY: Status,
          LABEL_CATEGORY: Label,
          TASK_CATEGORY: Task,
          USER_CATEGORY: User}

"""
@register.inclusion_tag('table_head.html')
def show_table_head(category=TASK_CATEGORY):
    return {'title': TITLES[category],
            'table_heads': TABLE_HEADS[category],
            'create_path': CREATE_LINKS[category]['name'],
            'create_path_name': CREATE_LINKS[category]['title']}
"""
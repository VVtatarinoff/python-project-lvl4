import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView
from task_manager.models import Status, Label, Task
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat

logger = logging.getLogger(__name__)


class LoginRequiredMessage(AccessMixin):
    login_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, _('You are not authorized. Please log in'))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserCanEditProfile(AccessMixin):
    login_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and kwargs['pk'] != self.request.user.id:
            messages.error(self.request, _('You have no authorization to handle this action'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


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
DELETE_LINKS = {STATUS_CATEGORY: 'delete_status',
                LABEL_CATEGORY: 'delete_label',
                TASK_CATEGORY: 'delete_task',
                USER_CATEGORY: 'delete_user'}
UPDATE_LINKS = {STATUS_CATEGORY: 'update_status',
                LABEL_CATEGORY: 'update_label',
                TASK_CATEGORY: 'update_task',
                USER_CATEGORY: 'update_user'}
MODELS = {STATUS_CATEGORY: Status,
          LABEL_CATEGORY: Label,
          TASK_CATEGORY: Task,
          USER_CATEGORY: User}

QUARIES = {STATUS_CATEGORY: Status.objects.values_list('id', 'name',
                                           'creation_date',
                                           named=True),
           LABEL_CATEGORY: Label.objects.values_list('id', 'name',
                                           'creation_date',
                                           named=True),
           TASK_CATEGORY: Task.objects.values_list('id', 'name', 'status__name',
                                           Concat('author__first_name',
                                                  Value(' '), 'author__last_name'),
                                           Concat('executor__first_name',
                                                  Value(' '), 'executor__last_name'),
                                           'creation_date',
                                           named=True),
           USER_CATEGORY: User.objects.values_list('id', 'username',
                                           Concat('first_name',
                                                  Value(' '), 'last_name'),
                                           'date_joined',
                                           named=True).exclude(
            is_superuser=True)
           }
DETAIL_VIEW = {STATUS_CATEGORY: None,
          LABEL_CATEGORY: None,
          TASK_CATEGORY: 2,
          USER_CATEGORY: None}
DETAIL_VIEW_PATH = {STATUS_CATEGORY: None,
          LABEL_CATEGORY: None,
          TASK_CATEGORY: 'tasks_detail',
          USER_CATEGORY: None}


class SimpleTableView(ListView):
    def __init__(self, category, *arg, **kwargs):
        super(SimpleTableView, self).__init__(*arg, **kwargs)
        self.template_name = 'table.html'
        self.context_object_name = 'table'
        self.category = category

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = TITLES[self.category]
        context['table_heads'] = TABLE_HEADS[self.category]
        context['create_path'] = CREATE_LINKS[self.category]['name']
        context['create_path_name'] = CREATE_LINKS[self.category]['title']
        context['update_link'] = UPDATE_LINKS[self.category]
        context['delete_link'] = DELETE_LINKS[self.category]
        context['detail'] = DETAIL_VIEW[self.category]
        context['detail_path'] = DETAIL_VIEW_PATH[self.category]
        return context

    def get_queryset(self):
        return QUARIES[self.category].all()

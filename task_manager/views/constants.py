from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _

from task_manager.models import Status, Label, Task

STATUS_CATEGORY = 'statuses'
LABEL_CATEGORY = 'labels'
TASK_CATEGORY = 'tasks'
USER_CATEGORY = 'users'

MODELS = {STATUS_CATEGORY: Status,
          LABEL_CATEGORY: Label,
          TASK_CATEGORY: Task,
          USER_CATEGORY: User}

TITLES = {STATUS_CATEGORY: _("Statuses"),
          LABEL_CATEGORY: _("Labels"),
          TASK_CATEGORY: _("Tasks"),
          USER_CATEGORY: _("Users")}

DELETE_TITLES = {STATUS_CATEGORY: _("Delete status"),
                 LABEL_CATEGORY: _("Delete label"),
                 TASK_CATEGORY: _("Delete task"),
                 USER_CATEGORY: _("Delete user")}

CREATE_TITLES = {STATUS_CATEGORY: _("Create status"),
                 LABEL_CATEGORY: _("Create label"),
                 TASK_CATEGORY: _("Create task"),
                 USER_CATEGORY: _("Registration")}

UPDATE_TITLES = {STATUS_CATEGORY: _("Change status"),
                 LABEL_CATEGORY: _("Change label"),
                 TASK_CATEGORY: _("Change task"),
                 USER_CATEGORY: _("Change user data")}

TABLE_HEADS = {STATUS_CATEGORY: ('ID', _('Name'), _('Creation date')),
               LABEL_CATEGORY: ('ID', _('Name'), _('Creation date')),
               TASK_CATEGORY: ('ID', _('Name'), _('Status'), _('Author'),
                               _('Executor'), _('Creation date')),
               USER_CATEGORY: ('ID', _('User name'),
                               _('Full name'), _('Creation date'))}

CREATE_LINKS = {STATUS_CATEGORY: 'create_status',
                LABEL_CATEGORY: 'create_label',
                TASK_CATEGORY: 'create_task',
                USER_CATEGORY: 'registration'}

DELETE_LINKS = {STATUS_CATEGORY: 'delete_status',
                LABEL_CATEGORY: 'delete_label',
                TASK_CATEGORY: 'delete_task',
                USER_CATEGORY: 'delete_user'}

UPDATE_LINKS = {STATUS_CATEGORY: 'update_status',
                LABEL_CATEGORY: 'update_label',
                TASK_CATEGORY: 'update_task',
                USER_CATEGORY: 'update_user'}

LIST_LINKS = {STATUS_CATEGORY: 'statuses',
              LABEL_CATEGORY: 'labels',
              TASK_CATEGORY: 'tasks',
              USER_CATEGORY: 'users'}

QUARIES_LIST_VIEW = {
    STATUS_CATEGORY: Status.objects.values_list('id', 'name',
                                                'creation_date',
                                                named=True),
    LABEL_CATEGORY:
        Label.objects.values_list('id', 'name',
                                  'creation_date',
                                  named=True),
    TASK_CATEGORY:
        Task.objects.values_list('id', 'name', 'status__name',
                                 Concat('author__first_name',
                                        Value(' '),
                                        'author__last_name'),
                                 Concat('executor__first_name',
                                        Value(' '),
                                        'executor__last_name'),
                                 'creation_date',
                                 named=True),
    USER_CATEGORY:
        User.objects.values_list('id', 'username',
                                 Concat('first_name',
                                        Value(' '),
                                        'last_name'),
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

DELETE_SUCCESS_MESSAGE = {
    STATUS_CATEGORY: _('Status was successfully deleted'),
    LABEL_CATEGORY: _('Label was successfully deleted'),
    TASK_CATEGORY: _('Task was successfully deleted'),
    USER_CATEGORY: _('User was successfully deleted')}

DELETE_CONSTRAINT_MESSAGE = {
    STATUS_CATEGORY:
        _('Unable to delete status as it is in use'),
    LABEL_CATEGORY:
        _('Unable to delete label as it is in use'),
    TASK_CATEGORY:
        _('The task may be deleted only by author'),
    USER_CATEGORY:
        _('Unable to delete user as it is in use')}

CREATE_SUCCESS_MESSAGE = {
    STATUS_CATEGORY: _('Status was successfully created'),
    LABEL_CATEGORY: _('Label was successfully created'),
    TASK_CATEGORY: _('Task was successfully created'),
    USER_CATEGORY: _('Successful registration')}

UPDATE_SUCCESS_MESSAGE = {
    STATUS_CATEGORY: _('Status was successfully changed'),
    LABEL_CATEGORY: _('Label was successfully changed'),
    TASK_CATEGORY: _('Task was successfully changed'),
    USER_CATEGORY: _('User data was changed')}

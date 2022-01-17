import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, RestrictedError
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView,
                                  CreateView, DeleteView, UpdateView)
from django.utils.translation import gettext as _

from .forms import TaskForm, TaskFilter
from task_manager.mixins import LoginRequiredMessage
from tasks.models import Task

logger = logging.getLogger(__name__)

LIST_TITLE = _("Tasks")
CREATE_TITLE = _("Create task")
DELETE_TITLE = _("Delete task")
UPDATE_TITLE = _("Change task")
DETAIL_TITLE = _("Task page")

LIST_VIEW = 'tasks'
UPDATE_VIEW = 'update_task'
DELETE_VIEW = 'delete_task'
CREATE_VIEW = 'create_task'
DETAIL_VIEW = 'tasks_detail'

MESSAGE_UPDATE_SUCCESS = _('Task was successfully changed')
MESSAGE_DELETE_SUCCESS = _('Task was successfully deleted')
MESSAGE_CREATE_SUCCESS = _('Task was successfully created')
DELETE_CONSTRAINT_MESSAGE = _('The task may be deleted only by author')
QUESTION_DELETE = _('Are you sure you want to delete')
TABLE_HEADS = ('ID', _('Name'), _('Status'), _('Author'),
               _('Executor'), _('Creation date'))


class CreateTask(LoginRequiredMessage, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'form_view.html'
    model = Task
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLE
        context['btn_name'] = "Create"
        return context

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to assign task to a logged user"""
        kwargs = super(CreateTask, self).get_form_kwargs()
        kwargs['id'] = self.request.user.id
        return kwargs


class DeleteTask(LoginRequiredMessage, DeleteView):
    template_name = 'delete_page.html'
    model = Task
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_DELETE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = DELETE_TITLE
        context['btn_name'] = 'Yes, delete'
        name = self.get_object().get_full_name()
        msg = QUESTION_DELETE + ' ' + name + '?'
        context['message'] = msg
        return context

    def form_valid(self, form):
        try:
            self.object.delete()
        except RestrictedError:
            msg = DELETE_CONSTRAINT_MESSAGE
            messages.error(self.request, msg)
        else:
            messages.success(self.request,
                             self.success_message)
        return HttpResponseRedirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id and (
                self.get_object().author_id != self.request.user.id):
            messages.error(self.request,
                           DELETE_CONSTRAINT_MESSAGE)
            return redirect(LIST_VIEW)
        return super().dispatch(request, *args, **kwargs)


class TasksDetail(LoginRequiredMessage, DetailView):
    model = Task
    template_name = 'tasks/detail_view.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = DETAIL_TITLE
        context['update_link'] = UPDATE_VIEW
        context['delete_link'] = DELETE_VIEW
        return context


class UpdateTask(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    template_name = 'form_view.html'
    model = Task
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UPDATE_TITLE
        context['btn_name'] = "Change"
        return context

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display
         members that belong to a given user"""

        kwargs = super().get_form_kwargs()
        kwargs['id'] = self.get_object().author_id
        return kwargs


class Tasks(LoginRequiredMessage, ListView):
    template_name = 'tasks/tasks_table.html'
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = LIST_TITLE
        context['table_heads'] = TABLE_HEADS
        context['create_path_name'] = CREATE_TITLE
        context['create_path'] = CREATE_VIEW
        context['update_link'] = UPDATE_VIEW
        context['delete_link'] = DELETE_VIEW
        context['detail'] = 2
        context['detail_path'] = DETAIL_VIEW
        context['filter'] = TaskFilter(self.request.GET,
                                       request=self.request,
                                       queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        return Task.objects.values_list('id', 'name', 'status__name',
                                        Concat('author__first_name',
                                               Value(' '),
                                               'author__last_name'),
                                        Concat('executor__first_name',
                                               Value(' '),
                                               'executor__last_name'),
                                        'creation_date',
                                        named=True)

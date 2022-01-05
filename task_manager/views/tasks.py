from django.contrib import messages
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, ListView

from task_manager.forms.statuses_forms import CreateStatusForm, CreateLabelForm, CreateTaskForm
from task_manager.views.general import LoginRequiredMessage
from task_manager.models import Task
from task_manager.views.general import QUARIES, TITLES, TABLE_HEADS
from task_manager.views.general import CREATE_LINKS, UPDATE_LINKS,DELETE_LINKS


class Tasks(LoginRequiredMessage, ListView):
    model = Task
    template_name = 'table.html'
    context_object_name = 'table'

    def get_context_data(self, object_list=None, **kwargs):
        category = 'tasks'
        context = super().get_context_data(**kwargs)
        context['title'] = TITLES[category]
        context['table_heads'] = TABLE_HEADS[category]
        context['create_path'] = CREATE_LINKS[category]['name']
        context['create_path_name'] = CREATE_LINKS[category]['title']
        context['update_link'] = UPDATE_LINKS[category]
        context['delete_link'] = DELETE_LINKS[category]
        context['cat'] = category
        return context

    def get_queryset(self):
        return QUARIES['tasks']


class CreateTask(CreateView):
    template_name = 'authorization.html'
    form_class = CreateTaskForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create task"
        context['btn_name'] = "Create"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task was successfully created'))
        return reverse_lazy('tasks')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CreateTask, self).get_form_kwargs()
        print(kwargs)
        kwargs['id'] = self.request.user.id
        return kwargs


def del_task(request):
    return render(request, "main.html")


class ChangeTask(UpdateView):
    form_class = CreateTaskForm
    template_name = 'authorization.html'
    model = Task

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change label"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label was successfully changed'))
        return reverse_lazy('labels')

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from task_manager.forms.statuses_forms import CreateStatusForm, CreateLabelForm, CreateTaskForm
from task_manager.views.general import LoginRequiredMessage
from task_manager.models import Task
from task_manager.views.general import TableView


class Tasks(LoginRequiredMessage, TableView):
    def __init__(self):
        kwargs = dict()
        kwargs['model'] = Task
        kwargs['title'] = "Tasks"
        kwargs['update_link'] = 'update_task'
        kwargs['delete_link'] = 'delete_task'
        kwargs['table_heads'] = ('ID', _('Name'), _('Status'), _('Author'), _('Executor'), _('Creation date'))
        kwargs['create_link'] = 'create_task'
        kwargs['create_title'] = _('Create task')
        super().__init__(**kwargs)

    def get_queryset(self):
        q = self.model.objects.values_list('id', 'name', 'status', 'author', 'executor',
                                           'creation_date',
                                           named=True)
        return q


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
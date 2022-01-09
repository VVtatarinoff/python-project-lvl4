import logging

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, FormView, DetailView, DeleteView

from task_manager.forms.statuses_forms import CreateTaskForm, FilterTaskForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView, SimpleDelete
from task_manager.models import Task
from task_manager.views.general import TASK_CATEGORY, UPDATE_LINKS, DELETE_LINKS

logger = logging.getLogger(__name__)


class FilterTaskMixin(LoginRequiredMessage, FormView):
    model = Task
    form_class = FilterTaskForm
    filter_Q = {'status': Q(),
                'executor': Q(),
                'labels': Q(),
                'self_tasks': Q()}
    filtered_data = {'status': '',
                     'executor': '',
                     'labels': '',
                     'self_tasks': False}

    def get_form_kwargs(self):
        kwargs = super(FilterTaskMixin, self).get_form_kwargs()
        kwargs['initial'].update(self.filtered_data)
        return kwargs

    def get(self, request, *args, **kwargs):
        for key, value in self.filtered_data.items():
            if key == 'self_tasks':
                self.filtered_data[key] = bool(request.GET.get(key, 0))
            else:
                self.filtered_data[key] = request.GET.get(key, 0)
        self.filter_Q['status'] = Q(status=self.filtered_data['status']) if self.filtered_data['status'] else Q()
        self.filter_Q['executor'] = Q(executor=self.filtered_data['executor']) if self.filtered_data[
            'executor'] else Q()
        self.filter_Q['labels'] = Q(labels=self.filtered_data['labels']) if self.filtered_data['labels'] else Q()
        self.filter_Q['self_tasks'] = Q(author=request.user.id) if self.filtered_data['self_tasks'] else Q()
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        status_query = super().get_queryset(*args, **kwargs)
        status_query = status_query.filter(self.filter_Q['status'])
        status_query = status_query.filter(self.filter_Q['executor'])
        status_query = status_query.filter(self.filter_Q['labels'])
        status_query = status_query.filter(self.filter_Q['self_tasks'])
        return status_query


class Tasks(FilterTaskMixin, SimpleTableView):

    def __init__(self, *arg, **kwargs):
        super(Tasks, self).__init__(TASK_CATEGORY, *arg, **kwargs)


class CreateTask(CreateView):
    template_name = 'form_view.html'
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
        kwargs['id'] = self.request.user.id
        return kwargs


class DeleteTask(SimpleDelete):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and self.get_object().author_id != self.request.user.id:
            messages.error(self.request, _('The task may be deleted only by author'))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class TasksDetail(DetailView):
    model = Task
    template_name = 'detail_view.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Task page"
        context['update_link'] = UPDATE_LINKS[TASK_CATEGORY]
        context['delete_link'] = DELETE_LINKS[TASK_CATEGORY]
        return context


class ChangeTask(UpdateView):
    form_class = CreateTaskForm
    template_name = 'form_view.html'
    model = Task

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change task"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task was successfully changed'))
        return reverse_lazy('tasks')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(ChangeTask, self).get_form_kwargs()
        kwargs['id'] = self.request.user.id
        return kwargs

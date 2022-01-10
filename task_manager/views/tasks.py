import logging

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView

from task_manager.forms.other_forms import CreateTaskForm, FilterTaskForm
from task_manager.views.constants import DELETE_CONSTRAINT_MESSAGE, LIST_LINKS
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.views.general import SimpleDelete, CreateMixin, UpdateMixin
from task_manager.models import Task
from task_manager.views.general import TASK_CATEGORY, UPDATE_LINKS
from task_manager.views.general import DELETE_LINKS

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
        for key in self.filtered_data:
            received = request.GET.get(key, 0)
            self.filtered_data[key] = bool(received) if key == 'self_tasks'\
                else received
        self.filter_Q['status'] = Q(status=self.filtered_data['status']) \
            if self.filtered_data['status'] else Q()
        self.filter_Q['executor'] = Q(executor=self.filtered_data['executor'])\
            if self.filtered_data['executor'] else Q()
        self.filter_Q['labels'] = Q(labels=self.filtered_data['labels'])\
            if self.filtered_data['labels'] else Q()
        self.filter_Q['self_tasks'] = Q(author=request.user.id)\
            if self.filtered_data['self_tasks'] else Q()
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        status_query = super().get_queryset(*args, **kwargs)
        for q in self.filter_Q.values():
            status_query = status_query.filter(q)
        return status_query


class Tasks(FilterTaskMixin, SimpleTableView):
    pass


class CreateTask(CreateMixin):
    form_class = CreateTaskForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to assign task to a logged user"""

        kwargs = super(CreateTask, self).get_form_kwargs()
        kwargs['id'] = self.request.user.id
        return kwargs


class DeleteTask(SimpleDelete):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id and (
                self.get_object().author_id != self.request.user.id):
            messages.error(self.request,
                           DELETE_CONSTRAINT_MESSAGE[TASK_CATEGORY])
            return redirect(LIST_LINKS[TASK_CATEGORY])
        return super().dispatch(request, *args, **kwargs)


class TasksDetail(LoginRequiredMessage, DetailView):
    model = Task
    template_name = 'detail_view.html'
    context_object_name = 'task'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Task page"
        context['update_link'] = UPDATE_LINKS[TASK_CATEGORY]
        context['delete_link'] = DELETE_LINKS[TASK_CATEGORY]
        return context


class UpdateTask(UpdateMixin):
    form_class = CreateTaskForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display
         members that belong to a given user"""

        kwargs = super().get_form_kwargs()
        kwargs['id'] = self.get_object().author_id
        return kwargs

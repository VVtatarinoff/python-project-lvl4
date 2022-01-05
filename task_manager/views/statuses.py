from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from task_manager.forms.statuses_forms import CreateStatusForm
from task_manager.views.general import LoginRequiredMessage
from task_manager.models import Status
from task_manager.views.general import TableView


class Statuses(LoginRequiredMessage, TableView):
    def __init__(self):
        kwargs = dict()
        kwargs['model'] = Status
        kwargs['title'] = "Statuses"
        kwargs['update_link'] = 'update_status'
        kwargs['delete_link'] = 'delete_status'
        kwargs['table_heads'] = ('ID', _('Name'), _('Creation date'))
        kwargs['create_link'] = 'create_status'
        kwargs['create_title'] = _('Create status')
        super().__init__(**kwargs)

    def get_queryset(self):
        q = self.model.objects.values_list('id', 'name',
                                           'creation_date',
                                           named=True)
        return q


class CreateStatus(CreateView):
    template_name = 'authorization.html'
    form_class = CreateStatusForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create status"
        context['btn_name'] = "Create"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status was successfully created'))
        return reverse_lazy('statuses')


def del_status(request):
    return render(request, "main.html")


class ChangeStatus(UpdateView):
    form_class = CreateStatusForm
    template_name = 'authorization.html'
    model = Status

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change status"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status was successfully changed'))
        return reverse_lazy('statuses')
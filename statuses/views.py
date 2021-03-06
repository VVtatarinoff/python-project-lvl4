import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from .forms import StatusForm
from task_manager.mixins import LoginRequiredMessage
from statuses.models import Status

logger = logging.getLogger(__name__)

LIST_TITLE = _("Statuses")
CREATE_TITLE = _("Create status")
DELETE_TITLE = _("Delete status")
UPDATE_TITLE = _("Change status")

LIST_VIEW = 'statuses'
UPDATE_VIEW = 'update_status'
DELETE_VIEW = 'delete_status'
CREATE_VIEW = 'create_status'

MESSAGE_UPDATE_SUCCESS = _('Status was successfully changed')
MESSAGE_DELETE_SUCCESS = _('Status was successfully deleted')
MESSAGE_CREATE_SUCCESS = _('Status was successfully created')
DELETE_CONSTRAINT_MESSAGE = _('Unable to delete status as it is in use')
QUESTION_DELETE = _('Are you sure you want to delete')
TABLE_HEADS = ('ID', _('Name'), _('Creation date'))


class Statuses(LoginRequiredMessage, ListView):
    template_name = 'table.html'
    context_object_name = 'table'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = LIST_TITLE
        context['table_heads'] = TABLE_HEADS
        context['create_path_name'] = CREATE_TITLE
        context['create_path'] = CREATE_VIEW
        context['update_link'] = UPDATE_VIEW
        context['delete_link'] = DELETE_VIEW
        return context

    def get_queryset(self):
        return Status.objects.values_list('id', 'name',
                                          'creation_date',
                                          named=True)


class CreateStatus(LoginRequiredMessage, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'form_view.html'
    model = Status
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLE
        context['btn_name'] = "Create"
        return context


class UpdateStatus(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    template_name = 'form_view.html'
    model = Status
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UPDATE_TITLE
        context['btn_name'] = "Change"
        return context


class DeleteStatus(LoginRequiredMessage, DeleteView):
    template_name = 'delete_page.html'
    model = Status
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
            messages.success(self.request, MESSAGE_DELETE_SUCCESS)
        return HttpResponseRedirect(self.success_url)

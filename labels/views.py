import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from labels.forms import CreateLabelForm
from task_manager.models import Label
from task_manager.mixins import LoginRequiredMessage

logger = logging.getLogger(__name__)

LIST_TITLE = _("Labels")
CREATE_TITLE = _("Create label")
DELETE_TITLE = _("Delete label")
UPDATE_TITLE = _("Change label")

LIST_VIEW = 'labels'
UPDATE_VIEW = 'update_label'
DELETE_VIEW = 'delete_label'
CREATE_VIEW = 'create_label'

MESSAGE_UPDATE_SUCCESS = _('Label was successfully changed')
MESSAGE_DELETE_SUCCESS = _('Label was successfully deleted')
MESSAGE_CREATE_SUCCESS = _('Label was successfully created')
DELETE_CONSTRAINT_MESSAGE = _('Unable to delete label as it is in use')
QUESTION_DELETE = _('Are you sure you want to delete')
TABLE_HEADS = ('ID', _('Name'), _('Creation date'))


class Labels(LoginRequiredMessage, ListView):
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
        return Label.objects.values_list('id', 'name',
                                         'creation_date',
                                         named=True)


class CreateLabel(LoginRequiredMessage, SuccessMessageMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'form_view.html'
    model = Label
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLE
        context['btn_name'] = "Create"
        return context


class UpdateLabel(LoginRequiredMessage, SuccessMessageMixin, UpdateView):
    form_class = CreateLabelForm
    template_name = 'form_view.html'
    model = Label
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UPDATE_TITLE
        context['btn_name'] = "Change"
        return context


class DeleteLabel(LoginRequiredMessage, DeleteView):
    template_name = 'delete_page.html'
    model = Label
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

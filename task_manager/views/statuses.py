import logging

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from task_manager.forms.statuses_forms import CreateStatusForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.models import Status
from task_manager.views.general import STATUS_CATEGORY

logger = logging.getLogger(__name__)


class Statuses(LoginRequiredMessage, SimpleTableView):
    def __init__(self,*arg, **kwargs):
        super(Statuses, self).__init__(STATUS_CATEGORY, *arg, **kwargs)


class CreateStatus(CreateView):
    template_name = 'form_view.html'
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
    template_name = 'form_view.html'
    model = Status

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change status"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status was successfully changed'))
        return reverse_lazy('statuses')
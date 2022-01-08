import logging

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from task_manager.forms.statuses_forms import CreateLabelForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.models import Label
from task_manager.views.general import LABEL_CATEGORY

logger = logging.getLogger(__name__)


class Labels(LoginRequiredMessage, SimpleTableView):
    def __init__(self, *args, **kwargs):
        super(Labels, self).__init__(LABEL_CATEGORY, *args, **kwargs)


class CreateLabel(CreateView):
    template_name = 'form_view.html'
    form_class = CreateLabelForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create label"
        context['btn_name'] = "Create"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label was successfully created'))
        return reverse_lazy('labels')


def del_label(request):
    return render(request, "main.html")


class ChangeLabel(UpdateView):
    form_class = CreateLabelForm
    template_name = 'form_view.html'
    model = Label

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change label"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label was successfully changed'))
        return reverse_lazy('labels')
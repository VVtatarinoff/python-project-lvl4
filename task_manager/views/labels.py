from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView

from task_manager.forms.statuses_forms import CreateLabelForm
from task_manager.views.general import LoginRequiredMessage
from task_manager.models import Label
from task_manager.views.general import TableView


class Labels(LoginRequiredMessage, TableView):
    def __init__(self):
        kwargs = dict()
        kwargs['model'] = Label
        kwargs['title'] = "Labels"
        kwargs['update_link'] = 'update_label'
        kwargs['delete_link'] = 'delete_label'
        kwargs['table_heads'] = ('ID', _('Name'), _('Creation date'))
        kwargs['create_link'] = 'create_label'
        kwargs['create_title'] = _('Create label')
        super().__init__(**kwargs)

    def get_queryset(self):
        q = self.model.objects.values_list('id', 'name',
                                           'creation_date',
                                           named=True)
        return q


class CreateLabel(CreateView):
    template_name = 'authorization.html'
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
    template_name = 'authorization.html'
    model = Label

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change label"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label was successfully changed'))
        return reverse_lazy('labels')
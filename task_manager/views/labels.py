from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, ListView

from task_manager.forms.statuses_forms import CreateLabelForm
from task_manager.views.general import LoginRequiredMessage
from task_manager.models import Label
from task_manager.views.general import QUARIES, TITLES, TABLE_HEADS
from task_manager.views.general import CREATE_LINKS, UPDATE_LINKS,DELETE_LINKS


class Labels(LoginRequiredMessage, ListView):
    model = Label
    template_name = 'table.html'
    context_object_name = 'table'

    def get_context_data(self, object_list=None, **kwargs):
        category = 'labels'
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
        return QUARIES['labels']


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
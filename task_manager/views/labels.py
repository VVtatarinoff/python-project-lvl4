import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView

from task_manager.forms.statuses_forms import CreateLabelForm
from task_manager.views.general import LoginRequiredMessage, SimpleTableView
from task_manager.models import Label, Task
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


class DeleteLabel(DeleteView):
    model = Label
    template_name = 'delete_page.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete label"
        context['btn_name'] = 'Yes, delete'
        name = self.get_object().name
        msg = _('Are you sure you want to delete') + ' ' + name + '?'
        context['message'] = msg
        return context

    def form_valid(self, form):
        object = self.get_object()
        inclusion = Task.objects.filter(labels=object.id).first()
        if inclusion:
            msg = _('Unable to delete label as it is in use')
            messages.error(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('labels'))
        self.object.delete()
        messages.success(self.request, _('Label was successfully deleted'))
        return HttpResponseRedirect(reverse_lazy('labels'))


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
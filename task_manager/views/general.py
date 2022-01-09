import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DeleteView
from task_manager.models import Status, Label, Task
from django.contrib.auth.models import User
from django.db.models import Value, RestrictedError
from django.db.models.functions import Concat
from task_manager.views.constants import *

logger = logging.getLogger(__name__)


class LoginRequiredMessage(AccessMixin):
    login_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, _('You are not authorized. Please log in'))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserCanEditProfile(AccessMixin):
    login_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and kwargs['pk'] != self.request.user.id:
            messages.error(self.request, _('You have no authorization to handle this action'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class SimpleTableView(ListView):
    def __init__(self, category, *arg, **kwargs):
        super(SimpleTableView, self).__init__(*arg, **kwargs)
        self.template_name = 'table.html'
        self.context_object_name = 'table'
        self.category = category

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = TITLES[self.category]
        context['table_heads'] = TABLE_HEADS[self.category]
        context['create_path'] = CREATE_LINKS[self.category]['name']
        context['create_path_name'] = CREATE_LINKS[self.category]['title']
        context['update_link'] = UPDATE_LINKS[self.category]
        context['delete_link'] = DELETE_LINKS[self.category]
        context['detail'] = DETAIL_VIEW[self.category]
        context['detail_path'] = DETAIL_VIEW_PATH[self.category]
        return context

    def get_queryset(self):
        return QUARIES_LIST_VIEW[self.category].all()


class SimpleDelete(LoginRequiredMessage, DeleteView):
    template_name = 'delete_page.html'
    category = None
    model = None
    next_page = None

    def setup(self, request, *args, **kwargs):
        self.category = kwargs['category']
        self.model = MODELS[self.category]
        self.next_page = reverse_lazy(LIST_LINKS[self.category])
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = DELETE_TITLES[self.category]
        context['btn_name'] = 'Yes, delete'
        name = self.get_object().get_full_name()
        msg = _('Are you sure you want to delete') + ' ' + name + '?'
        context['message'] = msg
        return context

    def form_valid(self, form):
        try:
            self.object.delete()
        except RestrictedError:
            msg = DELETE_CONSTRAINT_MESSAGE[self.category]
            messages.error(self.request, msg)
        else:
            messages.success(self.request,
                             DELETE_SUCCESS_MESSAGE[self.category])
        return HttpResponseRedirect(self.next_page)

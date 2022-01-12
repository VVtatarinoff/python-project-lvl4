import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from django.db.models import RestrictedError
from task_manager.views.constants import *  # noqa 403

logger = logging.getLogger(__name__)


class LoginRequiredMessage(AccessMixin):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, FLASH_LOGINREQUIRED)  # noqa 405
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class UserCanEditProfile(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.id:
            messages.error(self.request,
                           (FLASH_NO_PERMISSION_EDIT))         # noqa 405
            return redirect(LIST_LINKS[USER_CATEGORY])          # noqa 405
        return super().dispatch(request, *args, **kwargs)


class SetupMixin(object):
    def setup(self, request, *args, **kwargs):
        self.category = kwargs['category']
        self.model = MODELS[self.category]  # noqa 405
        self.next_page = reverse_lazy(LIST_LINKS[self.category])  # noqa 405
        return super().setup(request, *args, **kwargs)


class SimpleTableView(ListView):
    category = None
    template_name = 'table.html'
    context_object_name = 'table'

    def setup(self, request, *args, **kwargs):
        self.category = kwargs['category']
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = TITLES[self.category]  # noqa 405
        context['table_heads'] = TABLE_HEADS[self.category]  # noqa 405
        if self.category != USER_CATEGORY:  # noqa 405
            context['create_path_name'] = CREATE_TITLES[self.category]  # noqa 405
            context['create_path'] = CREATE_LINKS[self.category]  # noqa 405
        context['update_link'] = UPDATE_LINKS[self.category]  # noqa 405
        context['delete_link'] = DELETE_LINKS[self.category]  # noqa 405
        context['detail'] = DETAIL_VIEW[self.category]  # noqa 405
        context['detail_path'] = DETAIL_VIEW_PATH[self.category]  # noqa 405
        return context

    def get_queryset(self):
        return QUARIES_LIST_VIEW[self.category].all()  # noqa 405


class SimpleDelete(LoginRequiredMessage, SetupMixin, DeleteView):
    template_name = 'delete_page.html'
    category = None
    model = None
    next_page = None

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = DELETE_TITLES[self.category]  # noqa 405
        context['btn_name'] = 'Yes, delete'
        name = self.get_object().get_full_name()
        msg = QUESTION_DELETE + ' ' + name + '?'        # noqa 405
        context['message'] = msg
        return context

    def form_valid(self, form):
        try:
            self.object.delete()
        except RestrictedError:
            msg = DELETE_CONSTRAINT_MESSAGE[self.category]  # noqa 405
            messages.error(self.request, msg)
        else:
            messages.success(self.request,
                             DELETE_SUCCESS_MESSAGE[self.category])  # noqa 405
        return HttpResponseRedirect(self.next_page)


class CreateMixin(LoginRequiredMessage, SetupMixin, CreateView):
    template_name = 'form_view.html'
    category = None
    next_page = None

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLES[self.category]  # noqa 405
        context['btn_name'] = "Create"
        return context

    def get_success_url(self):
        messages.success(self.request, CREATE_SUCCESS_MESSAGE[self.category])  # noqa 405
        return self.next_page


class UpdateMixin(LoginRequiredMessage, SetupMixin, UpdateView):
    template_name = 'form_view.html'
    model = None
    category = None
    next_page = None

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UPDATE_TITLES[self.category]  # noqa 405
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, UPDATE_SUCCESS_MESSAGE[self.category])  # noqa 405
        return self.next_page

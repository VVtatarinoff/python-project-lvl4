import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .forms import RegisterUserForm
from .forms import LoginUserForm, UpdateUserForm
from task_manager.mixins import LoginRequiredMessage

logger = logging.getLogger(__name__)

LIST_TITLE = _("Users")
CREATE_TITLE = _("Registration")
DELETE_TITLE = _("Delete user")
UPDATE_TITLE = _("Change user data")
LOGIN_TITLE = _("Authorization")

LIST_VIEW = 'users'
UPDATE_VIEW = 'update_user'
DELETE_VIEW = 'delete_user'
CREATE_VIEW = 'registration'

MESSAGE_UPDATE_SUCCESS = _('User data was changed')
MESSAGE_DELETE_SUCCESS = _('User was successfully deleted')
MESSAGE_CREATE_SUCCESS = _('Successful registration')
MESSAGE_LOGIN_SUCCESS = _('Successful login')
MESSAGE_LOGOUT_SUCCESS = _('You are logged out')
MESSAGE_INVALID_PASSWORD = _('Invalid pair user-password')
MESSAGE_NO_PERMISSION = _('You have no authorization to handle this action')
DELETE_CONSTRAINT_MESSAGE = _('Unable to delete user as it is in use')
QUESTION_DELETE = _('Are you sure you want to delete')
TABLE_HEADS = ('ID', _('User name'),
               _('Full name'), _('Creation date'))


class UserCanEditProfile(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.id:
            messages.error(self.request, MESSAGE_NO_PERMISSION)
            return redirect(reverse_lazy(LIST_VIEW))
        return super().dispatch(request, *args, **kwargs)


class UserList(ListView):
    template_name = 'table.html'
    context_object_name = 'table'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = LIST_TITLE
        context['table_heads'] = TABLE_HEADS
        context['update_link'] = UPDATE_VIEW
        context['delete_link'] = DELETE_VIEW
        return context

    def get_queryset(self):
        return User.objects.values_list('id', 'username',
                                        Concat('first_name',
                                               Value(' '),
                                               'last_name'),
                                        'date_joined',
                                        named=True).exclude(
            is_superuser=True)


class UpdateUser(LoginRequiredMessage, UserCanEditProfile,
                 SuccessMessageMixin, UpdateView):
    form_class = UpdateUserForm
    template_name = 'form_view.html'
    model = User
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_UPDATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = UPDATE_TITLE
        context['btn_name'] = _("Change")
        return context

    def get_success_url(self):
        logout(self.request)
        return super().get_success_url()


class DeleteUser(LoginRequiredMessage, UserCanEditProfile,
                 SuccessMessageMixin, DeleteView):
    template_name = 'delete_page.html'
    success_url = reverse_lazy(LIST_VIEW)
    success_message = MESSAGE_DELETE_SUCCESS
    model = User

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = DELETE_TITLE
        context['btn_name'] = _('Yes, delete')
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
            messages.success(self.request,
                             self.success_message)
        return HttpResponseRedirect(self.success_url)


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'form_view.html'
    success_url = reverse_lazy('login')
    success_message = MESSAGE_CREATE_SUCCESS

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLE
        context['btn_name'] = _("Register user")
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'form_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = LOGIN_TITLE
        context['btn_name'] = "Enter"
        return context

    def get_success_url(self):
        messages.success(self.request, MESSAGE_LOGIN_SUCCESS)
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, MESSAGE_INVALID_PASSWORD)
        return super().form_invalid(form)


class LogOut(LoginRequiredMessage, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, MESSAGE_LOGOUT_SUCCESS)
        return super().dispatch(request, *args, **kwargs)

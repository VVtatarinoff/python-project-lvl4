import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView

from task_manager.forms.users_forms import RegisterUserForm
from task_manager.forms.users_forms import LoginUserForm, ChangeUserForm
from task_manager.views.constants import CREATE_TITLES, USER_CATEGORY
from task_manager.views.constants import CREATE_SUCCESS_MESSAGE
from task_manager.views.general import UserCanEditProfile
from task_manager.views.general import SimpleDelete, UpdateMixin

logger = logging.getLogger(__name__)


class UpdateUser(UpdateMixin, UserCanEditProfile):
    form_class = ChangeUserForm

    def get_success_url(self):
        logout(self.request)
        return super().get_success_url()


class UserDelete(SimpleDelete, UserCanEditProfile):
    pass


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'form_view.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = CREATE_TITLES[USER_CATEGORY]
        context['btn_name'] = "Register user"
        return context

    def get_success_url(self):
        messages.success(self.request, CREATE_SUCCESS_MESSAGE[USER_CATEGORY])
        return reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'form_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Authorization"
        context['btn_name'] = "Enter"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Successful login'))
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid pair user-password'))
        return super().form_invalid(form)


class LogOut(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.edit import DeleteView

from task_manager.forms.users_forms import RegisterUserForm
from task_manager.forms.users_forms import LoginUserForm, ChangeUserForm
from task_manager.views.general import LoginRequiredMessage, UserCanEditProfile, SimpleTableView
from task_manager.views.general import USER_CATEGORY


class Users(SimpleTableView):
    def __init__(self,*arg, **kwargs):
        super(Users, self).__init__(USER_CATEGORY, *arg, **kwargs)


class UserUpdate(LoginRequiredMessage, UserCanEditProfile, UpdateView):
    form_class = ChangeUserForm
    template_name = 'authorization.html'
    model = User

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change user data"
        context['btn_name'] = "Change"
        return context

    def get_success_url(self):
        messages.success(self.request, _('User data was changed'))
        logout(self.request)
        return reverse_lazy('home')


class UserDelete(LoginRequiredMessage, UserCanEditProfile, DeleteView):
    template_name = 'delete_user.html'
    model = User
    user_to_delete = None
    id_to_delete = None

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete user"
        context['btn_name'] = 'Yes, delete'
        self.user_to_delete = self.get_object()
        full_name = f'{self.user_to_delete.first_name} ' \
                    f'{self.user_to_delete.last_name}'
        msg = _('Are you sure you want to delete') + ' ' + full_name + '?'
        context['message'] = msg
        return context

    def get_success_url(self):
        messages.success(self.request, _('User was successfully deleted'))
        logout(self.request)
        return reverse_lazy('users')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'authorization.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registration"
        context['btn_name'] = "Register user"
        return context

    def get_success_url(self):
        messages.success(self.request, _('Successful registration'))
        return reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'authorization.html'

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
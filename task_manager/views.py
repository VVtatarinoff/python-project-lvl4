from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView, DeleteView

from task_manager.forms import RegisterUserForm, LoginUserForm, ChangeUserForm


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


class Users(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Users"
        return context

    def get_queryset(self):
        return self.model.objects.all()


class Statuses(LoginRequiredMessage, ListView):
    template_name = 'main.html'


class Labels(LoginRequiredMessage, ListView):
    template_name = 'main.html'


class Tasks(LoginRequiredMessage, ListView):
    template_name = 'main.html'


class UserUpdate(LoginRequiredMessage, UserCanEditProfile, UpdateView):
    form_class = ChangeUserForm
    template_name = 'authorization.html'
    model = User

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change user data"
        context['btn_name'] = "Change"
        return context

    # def get_queryset(self):
    #    return self.model.objects.filter(id=self.request.user.id)

    def get_success_url(self):
        messages.success(self.request, _('User data was changed'))
        logout(self.request)
        return reverse_lazy('home')

#    def save(self, commit=True):
#        user = super().save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return


class UserDelete(LoginRequiredMessage, UserCanEditProfile, DeleteView):
    template_name = 'delete_user.html'
    model = User
    # form_class = DeleteUserForm
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

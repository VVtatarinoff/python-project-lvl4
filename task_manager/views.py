from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, TemplateView

from task_manager.forms import RegisterUserForm, LoginUserForm


class Index(TemplateView):
    template_name = 'main.html'


def users(request):
    return HttpResponse('Users')

def statuses(request):
    return HttpResponse('Statuses')

def labels(request):
    return HttpResponse('Labels')

def tasks(request):
    return HttpResponse('Tasks')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'authorization.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registration"
        context['btn_name'] = "Register user"
        return context
        # context = super().get_context_data(**kwargs)
    #    c_def = self.get_user_context(title="Registration")
        # return dict(list(context.items()) + list(c_def.items()))
    #    return c_def

    def get_success_url(self):
        messages.success(self.request, _('Successful registration'))
        return reverse_lazy('home')


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


def logout_user(request):
    logout(request)
    messages.info(request, _('You are logged out'))
    return redirect('home')
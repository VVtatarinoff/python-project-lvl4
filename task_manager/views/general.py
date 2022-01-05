from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView


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


class TableView(ListView):
    def __init__(self, model, title, update_link, delete_link, table_heads, create_link=None, create_title=None):
        super().__init__()
        self.model = model
        self.template_name = 'table.html'
        self.context_object_name = 'table'
        self.title = title
        self.update_link = update_link
        self.delete_link = delete_link
        self.table_heads = table_heads
        self.create_link = create_link
        self.create_title = create_title

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['update_link'] = self.update_link
        context['delete_link'] = self.delete_link
        context['create_link'] = self.create_link
        context['create_title'] = self.create_title
        context['table_heads'] = self.table_heads
        return context

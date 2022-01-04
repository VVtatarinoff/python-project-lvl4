from django.views.generic import ListView

from task_manager.views.general import LoginRequiredMessage


class Statuses(LoginRequiredMessage, ListView):
    template_name = 'main.html'
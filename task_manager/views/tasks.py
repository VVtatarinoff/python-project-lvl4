from django.views.generic import ListView

from task_manager.views.general import LoginRequiredMessage


class Tasks(LoginRequiredMessage, ListView):
    template_name = 'main.html'
"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

import task_manager.views.users as users
import task_manager.views.labels as labels
import task_manager.views.statuses as statuses
import task_manager.views.tasks as tasks
import task_manager.views.general as general
from task_manager.views.constants import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    path('users/', users.Users.as_view(), name='users'),
    path('login/', users.LoginUser.as_view(), name='login'),
    path('logout/', users.LogOut.as_view(), name='logout'),
    path('users/create/', users.RegisterUser.as_view(), name='registration'),
    path('statuses/', statuses.Statuses.as_view(), name='statuses'),
    path('labels/', labels.Labels.as_view(), name='labels'),
    path('tasks/', tasks.Tasks.as_view(), name='tasks'),
    path('tasks/<int:pk>/', tasks.TasksDetail.as_view(), name='tasks_detail'),
    path('users/<int:pk>/update/', users.UserUpdate.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', users.UserDelete.as_view(), name='delete_user'),
    path('statuses/<int:pk>/update/', statuses.ChangeStatus.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', general.SimpleDelete.as_view(),
         kwargs={'category': STATUS_CATEGORY}, name='delete_status'),
    path('statuses/create/', statuses.CreateStatus.as_view(), name='create_status'),
    path('labels/<int:pk>/update/', labels.ChangeLabel.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', general.SimpleDelete.as_view(),
         kwargs={'category': LABEL_CATEGORY}, name='delete_label'),
    path('labels/create/', labels.CreateLabel.as_view(), name='create_label'),
    path('tasks/<int:pk>/update/', tasks.ChangeTask.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', tasks.DeleteTask.as_view(), name='delete_task'),
    path('tasks/create/', tasks.CreateTask.as_view(), name='create_task'),

]

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

import task_manager.views.tasks as tasks
import labels.views
import statuses.views
from task_manager.views.constants import TASK_CATEGORY
from task_manager.views.constants import DELETE_LINKS, UPDATE_LINKS
from task_manager.views.constants import LIST_LINKS, CREATE_LINKS
import users.views

kwargs = dict()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    path('users/', users.views.UserList.as_view(),
         name=users.views.LIST_VIEW),
    path('login/', users.views.LoginUser.as_view(), name='login'),
    path('logout/', users.views.LogOut.as_view(), name='logout'),
    path('users/create/', users.views.CreateUser.as_view(),
         name=users.views.CREATE_VIEW),
    path('users/<int:pk>/update/', users.views.UpdateUser.as_view(),
         name=users.views.UPDATE_VIEW),
    path('users/<int:pk>/delete/', users.views.UserDelete.as_view(),
         name=users.views.DELETE_VIEW),

    path('statuses/', statuses.views.Statuses.as_view(),
         name=statuses.views.LIST_VIEW),
    path('statuses/<int:pk>/update/', statuses.views.UpdateStatus.as_view(),
         name=statuses.views.UPDATE_VIEW),
    path('statuses/<int:pk>/delete/', statuses.views.DeleteStatus.as_view(),
         name=statuses.views.DELETE_VIEW),
    path('statuses/create/', statuses.views.CreateStatus.as_view(),
         name=statuses.views.CREATE_VIEW),

    path('labels/', labels.views.Labels.as_view(),
         name=labels.views.LIST_VIEW),
    path('labels/<int:pk>/update/', labels.views.UpdateLabel.as_view(),
         name=labels.views.UPDATE_VIEW),
    path('labels/<int:pk>/delete/', labels.views.DeleteLabel.as_view(),
         name=labels.views.DELETE_VIEW),
    path('labels/create/', labels.views.CreateLabel.as_view(),
         name=labels.views.CREATE_VIEW),

    path('tasks/', tasks.Tasks.as_view(),
         kwargs={'category': TASK_CATEGORY},
         name=LIST_LINKS[TASK_CATEGORY]),
    path('tasks/<int:pk>/', tasks.TasksDetail.as_view(), name='tasks_detail'),
    path('tasks/<int:pk>/update/', tasks.UpdateTask.as_view(),
         kwargs={'category': TASK_CATEGORY},
         name=UPDATE_LINKS[TASK_CATEGORY]),
    path('tasks/<int:pk>/delete/', tasks.DeleteTask.as_view(),
         kwargs={'category': TASK_CATEGORY},
         name=DELETE_LINKS[TASK_CATEGORY]),
    path('tasks/create/', tasks.CreateTask.as_view(),
         kwargs={'category': TASK_CATEGORY},
         name=CREATE_LINKS[TASK_CATEGORY])
]

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

import labels.views
import statuses.views
import tasks.views
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

    path('tasks/', tasks.views.Tasks.as_view(),
         name=tasks.views.LIST_VIEW),
    path('tasks/<int:pk>/', tasks.views.TasksDetail.as_view(),
         name=tasks.views.DETAIL_VIEW),
    path('tasks/<int:pk>/update/', tasks.views.UpdateTask.as_view(),
         name=tasks.views.UPDATE_VIEW),
    path('tasks/<int:pk>/delete/', tasks.views.DeleteTask.as_view(),
         name=tasks.views.DELETE_VIEW),
    path('tasks/create/', tasks.views.CreateTask.as_view(),
         name=tasks.views.CREATE_VIEW)
]

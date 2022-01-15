from django.urls import path

import tasks.views as views


urlpatterns = [
    path('', views.Tasks.as_view(),
         name=views.LIST_VIEW),
    path('<int:pk>/', views.TasksDetail.as_view(),
         name=views.DETAIL_VIEW),
    path('<int:pk>/update/', views.UpdateTask.as_view(),
         name=views.UPDATE_VIEW),
    path('<int:pk>/delete/', views.DeleteTask.as_view(),
         name=views.DELETE_VIEW),
    path('create/', views.CreateTask.as_view(),
         name=views.CREATE_VIEW)
]

from django.urls import path

import statuses.views as views


urlpatterns = [
    path('', views.Statuses.as_view(),
         name=views.LIST_VIEW),
    path('<int:pk>/update/', views.UpdateStatus.as_view(),
         name=views.UPDATE_VIEW),
    path('<int:pk>/delete/', views.DeleteStatus.as_view(),
         name=views.DELETE_VIEW),
    path('create/', views.CreateStatus.as_view(),
         name=views.CREATE_VIEW)
]

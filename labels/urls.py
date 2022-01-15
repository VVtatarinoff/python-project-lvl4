from django.urls import path

import labels.views as views


urlpatterns = [
    path('', views.Labels.as_view(),
         name=views.LIST_VIEW),
    path('<int:pk>/update/', views.UpdateLabel.as_view(),
         name=views.UPDATE_VIEW),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(),
         name=views.DELETE_VIEW),
    path('create/', views.CreateLabel.as_view(),
         name=views.CREATE_VIEW)
]

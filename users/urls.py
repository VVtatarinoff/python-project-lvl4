from django.urls import path

import users.views as views


urlpatterns = [
    path('', views.UserList.as_view(),
         name=views.LIST_VIEW),
    path('<int:pk>/update/', views.UpdateUser.as_view(),
         name=views.UPDATE_VIEW),
    path('<int:pk>/delete/', views.DeleteUser.as_view(),
         name=views.DELETE_VIEW),
    path('create/', views.CreateUser.as_view(),
         name=views.CREATE_VIEW)
]
extra_patterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
]

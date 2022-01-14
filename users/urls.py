from django.urls import path

import users

urlpatterns = {
    path('users/', users.views.UserList.as_view(),
         name=users.views.LIST_VIEW),
    path('login/', users.views.LoginUser.as_view(), name='login'),
    path('logout/', users.views.LogOut.as_view(), name='logout'),
    path('users/create/', users.views.CreateUser.as_view(),
         name=users.views.CREATE_VIEW),
    path('users/<int:pk>/update/', users.views.UpdateUser.as_view(),
         name=users.views.UPDATE_VIEW),
    path('users/<int:pk>/delete/', users.views.UserDelete.as_view(),
         name=users.views.DELETE_VIEW)
}

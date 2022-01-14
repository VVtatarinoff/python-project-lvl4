from django.urls import path


urlpatterns = [
    path('users/', general.SimpleTableView.as_view(),
         name=LIST_LINKS[USER_CATEGORY]),
    path('login/', users.LoginUser.as_view(), name='login'),
    path('logout/', users.LogOut.as_view(), name='logout'),
    path('users/create/', users.RegisterUser.as_view(),
         name=CREATE_LINKS[USER_CATEGORY]),
    path('users/<int:pk>/update/', users.UpdateUser.as_view(),
         kwargs={'category': USER_CATEGORY},
         name=UPDATE_LINKS[USER_CATEGORY]),
    path('users/<int:pk>/delete/', users.UserDelete.as_view(),
         kwargs={'category': USER_CATEGORY},
         name=DELETE_LINKS[USER_CATEGORY]),

]
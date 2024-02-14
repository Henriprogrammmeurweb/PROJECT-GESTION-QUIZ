from django.urls import path
from .import views


urlpatterns=[
    path('', views.index, name='index'),
    path('account/sign-up', views.signUp, name='signUp'),
    path('account/login', views.loginUser, name='loginUser'),
    path('account/logout', views.logoutUser, name='logoutUser'),
    path('dasboard', views.dashboard, name='dashboard'),
    path('account/listeUser', views.listeUser, name="listeUser"),
    path('account/adminAddUser', views.adminAddUser, name="adminAddUser"),
    path('account/adminUpdateUser=<str:id>', views.adminUpdateUser, name='adminUpdateUser'),
    path('account/adminDeleteUser=<str:id>', views.adminDeleteUser, name='adminDeleteUser'),
    path('account/GetQuizUserPlay=<str:id>', views.GetQuizUserPlay, name="GetQuizUserPlay")
]
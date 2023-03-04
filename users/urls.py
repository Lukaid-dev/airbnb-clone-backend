from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),  # 이런 특정 rul이 re-url보다 위에 있어야함
    path("change-password/", views.ChangePassword.as_view()),
    # login coockie
    path("log-in/", views.LogIn.as_view()),
    path("log-out/", views.LogOut.as_view()),
    # login token
    path("token-login/", obtain_auth_token),
    # login jwt
    path("jwt-login/", views.JWTLogin.as_view()),
    path("@<str:username>/", views.PublicUser.as_view()),
]

from django.urls import path

from .views import *

urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
]


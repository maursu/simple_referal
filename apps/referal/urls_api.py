from django.urls import path

from . import views

urlpatterns = [
    path("authorize/", views.AuthorizeUserView.as_view(), name="authorize"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]

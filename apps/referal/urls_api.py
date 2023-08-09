from django.urls import path

from . import views

urlpatterns = [
    path("authorize/", views.AuthorizeUserView.as_view(), name="authorize_api"),
    path("login/", views.LoginUserView.as_view(), name="login_api"),
    path("profile/", views.ProfileView.as_view(), name="profile_api"),
]

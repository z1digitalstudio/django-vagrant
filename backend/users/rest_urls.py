from django.urls import path

from .rest_views import (
    EditProfileRestView, ChangePasswordRestView
)

urlpatterns = [
    path(
        r'password/',
        ChangePasswordRestView.as_view(),
        name="change_password"),
    path(
        r'profile/',
        EditProfileRestView.as_view(),
        name="edit_profile")
]

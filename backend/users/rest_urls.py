from django.conf.urls import url

from users.rest_views import (
    EditProfileRestView, ChangePasswordRestView
)

urlpatterns = [
    url(
        r'^password/$',
        ChangePasswordRestView.as_view(),
        name="change_password"),
    url(
        r'^profile/$',
        EditProfileRestView.as_view(),
        name="edit_profile")
]

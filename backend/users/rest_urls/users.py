from django.urls import path

from users.rest_views import (ChangePasswordRestView,
                              UserListRestView, UserMeRetrieveRestView,
                              UserRetrieveUpdateRestView)

urlpatterns = [
    path("", UserListRestView.as_view(), name="list_users"),
    path("<uuid:pk>/", UserRetrieveUpdateRestView.as_view(), name="get_profile"),
    path("me/", UserMeRetrieveRestView.as_view(), name="me"),
    path("password/", ChangePasswordRestView.as_view(), name="change_password"),
]

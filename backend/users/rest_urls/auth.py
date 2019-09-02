from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView)

from users.rest_views import (CustomTokenObtainPairView,
                              ChangePasswordRestView, ResetPasswordRestView,
                              ConfirmResetPasswordView)


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("password/", ChangePasswordRestView.as_view(),
         name="change_password"),
    path("reset-password/", ResetPasswordRestView.as_view(),
         name="reset_password"),
    path("confirm-password/<str:token>/", ConfirmResetPasswordView.as_view(),
         name="confirm_password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

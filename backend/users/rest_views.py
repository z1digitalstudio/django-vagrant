import os
import jwt
import datetime

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

from rest_framework import generics as api_views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (UserProfileSerializer, ChangePasswordSerializer,
                               CustomTokenObtainPairView, EmailField,
                               ResetPasswordSerializer)


class UserListRestView(api_views.ListCreateAPIView):
    """Return a list of Users"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserRetrieveUpdateRestView(api_views.RetrieveUpdateAPIView):
    """Return an specific user"""
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserMeRetrieveRestView(api_views.RetrieveUpdateAPIView):
    """Return logged user"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordRestView(api_views.UpdateAPIView):
    """Change logged user's password"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user

        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRestView(api_views.GenericAPIView):
    """Send an email for reseting the password"""
    serializer_class = EmailField

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.data["email"])
            email = serializer.data["email"]
            now = datetime.datetime.now()
            past = now + datetime.timedelta(hours=10)

            encoded_token = jwt.encode(
                {"user_id": str(user.id), "exp": past}, "secret", algorithm="HS256"
            )

            url = "%s/reset-password/%s" % (
                os.getenv("URL_FRONT"),
                encoded_token.decode("utf-8"),
            )
            subject = "You have requested to retrieve the password"
            message = (
                "You have received this email because you have requested a change of password,"
                " access this url %s and get your new password" % url
            )
            print(message)
            try:
                send_mail(
                    subject,
                    message,
                    "z1@z1.digital",
                    [email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response("The user does not exist", status=status.HTTP_403_FORBIDDEN)


class ConfirmResetPasswordView(api_views.UpdateAPIView):
    """Change the password of the user using the token provided in the url of the email to reset the password"""
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()
    decoded_token = None

    def _get_user(self):
        try:
            user = User.objects.get(id=self.decoded_token["user_id"])
        except User.DoesNotExist:
            return self.permission_denied(self.request, "The user does not exist")
        return user

    def get_object(self, *args, **kwargs):
        user = self._get_user()
        return user

    def perform_update(self, serializer):
        user = self.get_object()
        serializer.is_valid()
        user.set_password(serializer.validated_data['password'])
        user.save()

    def check_permission(self, request):
        try:
            self.decoded_token = jwt.decode(self.kwargs.get("token"), "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise self.permission_denied(request, "The token has expired")
        except jwt.InvalidTokenError:
            raise self.permission_denied(request, "The token is invalid")

    def update(self, request, *args, **kwargs):
        self.check_permission(request)
        return super(ConfirmResetPasswordView, self).update(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairView

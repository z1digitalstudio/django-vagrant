from rest_framework import generics as api_views
from rest_framework import permissions
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserProfileSerializer


class EditProfileRestView(api_views.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user


class ChangePasswordRestView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        if not(request.data.get('password')):
            raise ValidationError({"password": "Password cannot be blank"})
        if not(request.data.get('confirm')) or (
                request.data.get('password') != request.data.get('confirm')):
            raise ValidationError({"confirm": "Passwords must match"})
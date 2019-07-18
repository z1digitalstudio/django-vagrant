from rest_framework import generics as api_views
from rest_framework import permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserProfileSerializer, ChangePasswordSerializer
from rest_framework import status


class EditProfileRestView(api_views.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserProfileSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user


class ChangePasswordRestView(api_views.UpdateAPIView):
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
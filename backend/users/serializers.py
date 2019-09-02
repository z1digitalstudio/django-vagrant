from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = super(UserProfileSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'location', 'avatar')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    def update(self, instance, validated_data):
        pass

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class EmailField(serializers.Serializer):
    email = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    repeat_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data.get("password") != data.get("repeat_password"):
            raise serializers.ValidationError(
                {"password": ["Password must match"]}
            )
        return data


class CustomTokenObtainPairView(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data['user'] = token['user_id']

        return data

    class Meta:
        fields = ('first_name', 'last_name')

"""
Serializers for the user API View.
"""
from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name','phone','is_verified','groups']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        groups = validated_data.pop('groups',[])
        user = get_user_model().objects.create_user(**validated_data)

        # Add the user to the specified groups
        if groups:
            user.groups.set(groups)
        """Create and return a user with encrypted password."""
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for the user auth token."""
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#     )

#     def validate(self, attrs):
#         """Validate and authenticate the user."""
#         email = attrs.get('email')
#         password = attrs.get('password')
#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password,
#         )
#         if not user:
#             msg = _('Unable to authenticate with provided credentials.')
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return attrs
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(token)
        return token
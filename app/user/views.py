"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from user.serializers import (MyTokenObtainPairSerializer,
    UserSerializer,

)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from core.models import OTP
from django.contrib.auth import authenticate
from .utils import generate_and_send_otp,send_sms_otp
from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
User = get_user_model()
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Save the user
        user = serializer.save()

        # Generate and send OTP after user creation
        send_sms_otp(user)

        return user


# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for user."""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    print(serializer_class)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


@api_view(['POST'])
def verify_otp(request):
    # Get data from request
    username = request.data.get('username')
    otp = request.data.get('otp')
    # Get the user
    try:
        user = User.objects.get(email=username)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if OTP exists for this user
    otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()

    # Check if OTP is expired or invalid
    if not otp_obj or otp_obj.is_expired():
        return Response({'detail': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if OTP matches
    if otp_obj.otp != otp:
        return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    # OTP is valid, proceed to login or sign up
    # You can authenticate the user or create a new user here if needed
    user = authenticate(username=username, password=request.data.get('password'))
    if user is not None:
        return Response({'detail': 'OTP verified and user logged in'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

"""
URL mappings for the user API.
"""
from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
   TokenRefreshView,
)

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('otp-verify/', views.verify_otp, name='otp-verify')
]

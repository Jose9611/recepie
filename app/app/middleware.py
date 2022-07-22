from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from core.models import User
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.contrib.auth.middleware import get_user
import jwt
import json
import os

key = os.environ.get('SECRET_KEY', 'changeme')
class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    @staticmethod
    def get_jwt_user(request):
        user_jwt = get_user(request)
        if user_jwt.is_authenticated:
            return user_jwt
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_jwt = None
        if token is not None:
            try:
                user_jwt = jwt.decode(
                    token,
                    key,
                    algorithms=['HS256']
                )
                user_jwt = User.objects.get(
                    id=user_jwt['user_id']

                )
                if user_jwt is None:
                    raise exceptions.AuthenticationFailed('User not found')

                if not user_jwt.is_active:
                    raise exceptions.AuthenticationFailed('user is inactive')

            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason,"hiii")
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        return user_jwt

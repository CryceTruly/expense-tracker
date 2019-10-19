import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """returns the user object and token."""
        auth_header = authentication.get_authorization_header(request).split()

        if len(auth_header) == 2:
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')
            if prefix.lower() != 'Bearer'.lower():
                raise exceptions.AuthenticationFailed(
                    "Bearer needed as a prefix."
                )
            elif not ((self.authentication_credentials(request, token))[0]).is_verified:
                raise exceptions.AuthenticationFailed(
                    "Your email is not verified, please check your email."
                )
            return self.authentication_credentials(request, token)
        return None

    def authentication_credentials(self, request, token):
        """returns the decoded token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                raise exceptions.AuthenticationFailed(
                    "Your account was deactivated, please contact admin."
                )
            return (user, token)
        except:
            raise exceptions.AuthenticationFailed(
                "Your token is invalid or is expired, please login again."
            )

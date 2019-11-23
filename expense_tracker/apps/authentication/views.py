from rest_framework import status, generics, serializers
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer,
)

from ..core.utils import Utilities


class RegistrationAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        message = [
            request,
            "verify",
            user_data.get('token'),
            "Confirm Your Email Address",
            "created an expense tracker account.",
            user_data['email']
        ]
        Utilities.send_email(message, None, 'auth')

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.DecodeError:
            return self.sendResponse("verification link is invalid")
        except jwt.ExpiredSignatureError:
            return self.sendResponse("verification link is expired")
        user = User.objects.filter(email=payload.get('email')).first()
        user.is_verified = True
        user.save()
        # TODO UPdate with a redirect
        return self.sendResponse('Account activation successfull', 200)

    def sendResponse(self, message, status=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message}, status)


class PasswordResetAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    # then send rest password link
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        domain = request.META.get(
            'HTTP_ORIGIN', get_current_site(request).domain)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.filter(email=request.data['email'])
            if not user:
                raise serializers.ValidationError({
                    "email": ["No records correspodingto this user were found"]
                })

            message = [
                request,
                "reset-password/change/",
                str((jwt.encode({"email": request.data['email']},
                                settings.SECRET_KEY)).decode('utf-8')
                    ),
                "Reset Password",
                "requested for password reset.",
                request.data['email']
            ]

            Utilities.send_email(message, domain, 'password_reset')
            return Response(
                {
                    "message":
                    "Please check your email for the reset password link."
                },
                status.HTTP_200_OK
            )
        except KeyError:
            return Response({
                "errors": {
                    "email": ["Email is required to reset a password"]
                }},
                status.HTTP_400_BAD_REQUEST
            )

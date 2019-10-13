from rest_framework import status, generics, exceptions
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .renderers import UserJSONRenderer
import os
from django.http import HttpResponseRedirect
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer, ChangePasswordSerializer
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
            "created an account on Authors heaven.",
            user_data['email']
        ]
        Utilities.send_email(message,None,'auth')

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
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyAPIView(generics.GenericAPIView):
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
        domain = os.environ.get('FRONT_END_URL','localhost')
        return HttpResponseRedirect(domain)

    def sendResponse(self, message, status=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message}, status)


class PasswordResetAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    #then send rest password link
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        domain=request.META.get('HTTP_ORIGIN', get_current_site(request).domain)


        try:
            get_object_or_404(User, email=request.data['email'])
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


            Utilities.send_email(message,domain,'password_rest')
            return Response(
                {
                    "message": "Please check your email for the reset password link."
                },
                status.HTTP_200_OK
            )
        except KeyError:
            raise exceptions.ValidationError(
                "Email is required in order to reset password."
            )


class ChangePasswordAPIView(generics.GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    # then allows users to set password
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def patch(self, request):
        try:
            payload = jwt.decode(request.GET.get('token'), settings.SECRET_KEY)
            user = User.objects.filter(email=payload.get('email')).first()
            if len(request.data['password']) >= 8:
                user.set_password(request.data['password'])
                user.save()
                return Response({
                    "message": "you have reset your password successfully."},
                    status.HTTP_200_OK
                )
            return Response({
                "error": "password should be atleast 8 characters."},
                status.HTTP_400_BAD_REQUEST
            )

        except jwt.exceptions.DecodeError:
            return Response({
                "error": "verification link is invalid."},
                status.HTTP_400_BAD_REQUEST
            )
        except KeyError:
            raise exceptions.ValidationError("Password field is required.")
        except jwt.ExpiredSignatureError:
            return Response({
                "error": "verification link is expired"},
                status.HTTP_400_BAD_REQUEST
            )

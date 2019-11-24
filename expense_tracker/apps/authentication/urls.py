from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView, PasswordResetAPIView)
urlpatterns = [
    path('users/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    path('auth/register', RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'auth/reset-password/',
        PasswordResetAPIView.as_view(),
        name='reset_password_link'
    ),
]

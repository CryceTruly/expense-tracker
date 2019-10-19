from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView, PasswordResetAPIView, ChangePasswordAPIView)
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    path('auth/register', RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'auth/reset-password/',
        PasswordResetAPIView.as_view(),
        name='reset_password_link'
    ),
    path(
        'auth/reset-password/change/',
        ChangePasswordAPIView.as_view(),
        name='change_password'
    )
]
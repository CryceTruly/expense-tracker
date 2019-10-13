from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView, PasswordResetAPIView, ChangePasswordAPIView)
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
    path('users/register', RegistrationAPIView.as_view(), name='registration'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'users/reset-password/',
        PasswordResetAPIView.as_view(),
        name='reset_password_link'
    ),
    path(
        'users/reset-password/change/',
        ChangePasswordAPIView.as_view(),
        name='change_password'
    )
]

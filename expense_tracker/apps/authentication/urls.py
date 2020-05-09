from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView, PasswordResetAPIView)
urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('register', RegistrationAPIView.as_view(), name='registration'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('verify', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'reset-password',
        PasswordResetAPIView.as_view(),
        name='reset_password_link'
    ),
]

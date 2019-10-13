from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerifyAPIView, PasswordResetAPIView, ChangePasswordAPIView)
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='viewusers'),
<<<<<<< HEAD
    path('auth/register', RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'auth/reset-password/',
=======
    path('users/register', RegistrationAPIView.as_view(), name='registration'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/verify/', EmailVerifyAPIView.as_view(), name='verify_email'),
    path(
        'users/reset-password/',
>>>>>>> feat(accounts): Implement Account management
        PasswordResetAPIView.as_view(),
        name='reset_password_link'
    ),
    path(
<<<<<<< HEAD
        'auth/reset-password/change/',
=======
        'users/reset-password/change/',
>>>>>>> feat(accounts): Implement Account management
        ChangePasswordAPIView.as_view(),
        name='change_password'
    )
]

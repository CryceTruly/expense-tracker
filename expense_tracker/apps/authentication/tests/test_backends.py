"""User backends tests."""
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import valid_user
from ..models import User


class UserBackendsTest(BaseTest):

    def test_email_not_verified(self):
        """
        Tests if user is restricted from accessing
        get users routes when his/her email is not verified.
        """
        registration = self.client.post(
            self.registration_url,
            valid_user, format='json'
        )
        token = registration.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        response = self.client.get(self.viewusers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 
            "Your email is not verified, please check your email."
        )

    def tests_wrong_prefix(self):
        """Tests if the user has provided a wrong prefix"""
        registration = self.client.post(
            self.registration_url,
            valid_user, format='json'
        )
        token = registration.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='token '+ token)

        response = self.client.get(self.viewusers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 
            "Bearer needed as a prefix."
        )

    def test_invalid_token(self):
        """Tests if the user has provided a wrong token"""
        registration = self.client.post(
            self.registration_url,
            valid_user, format='json'
        )
        token = registration.data['token'] + "sabgccadca"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        response = self.client.get(self.viewusers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 
            "Your token is invalid or is expired, please login again."
        )

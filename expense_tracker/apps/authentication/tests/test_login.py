"""user login tests"""
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import (valid_user, valid_login,
                        wrong_password, wrong_email, missing_password_data, missing_email_data)


class UserLoginTest(BaseTest):

    """Contains user login test methods."""

    def test_verified_user_can_login(self):
        """Tests if a user with valid credentials can login."""
        reg_data = self.client.post(self.registration_url, valid_user, format='json')
        self.client.get(self.verify_url + "?token=" + reg_data.data["token"], format='json')
        response = self.client.post(self.login_url, valid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactivated_user_cannot_login(self):
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(self.login_url, valid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

"""Base file containing setup"""


from rest_framework.test import APIClient, APITestCase
from .test_data import valid_user, valid_login, valid_login_two, valid_user_two
from django.urls import reverse
from .test_data import valid_user, valid_login, valid_login_two, valid_user_two


class BaseTest(APITestCase):
    """Contains test setup method."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:login')
        self.registration_url = reverse('authentication:registration')
        self.viewusers = reverse('authentication:viewusers')
        self.verify_url = reverse('authentication:verify_email')
        self.reset_password_url = reverse('authentication:reset_password_link')
        self.change_password_url = reverse('authentication:change_password')

    def register_and_login_user(self):
        """
        Creates an account and attaches a token to the auth header
        """
        register_response = self.client.post(
            self.registration_url, valid_user, format='json')
        self.client.get(self.verify_url+"?token=" +
                        register_response.data['token'], format='json')
        response = self.client.post(self.login_url, valid_login, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def register_and_login_new_user(self):
        """
        Creates a second account and attaches a token to the auth header
        """
        register_response = self.client.post(
            self.registration_url, valid_user_two, format='json')
        self.client.get(self.verify_url+"?token=" +
                        register_response.data['token'], format='json')
        response = self.client.post(
            self.login_url, valid_login_two, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

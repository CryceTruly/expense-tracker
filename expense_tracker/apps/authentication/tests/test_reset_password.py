"""Reset Password tests."""
import jwt
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import valid_user
from django.conf import settings


class ResetPasswordTest(BaseTest):

    def test_existing_email(self):
        """Tests if user email exists in the database."""
        response = self.client.post(
            self.reset_password_url, {"email": "joel@gmail.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")

    def test_send_password_link(self):
        """Tests if a reset password link is sent successfully."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.reset_password_url,
            {"email": "bagendadeogracious@gmail.com"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "Please check your email for the reset password link."
        )

    def test_email_key_error(self):
        """Tests if a user has a provided an email field."""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.reset_password_url,
            {"eml": "bagendadeogracious@gmail.com"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors'][0],
            "Email is required in order to reset password."
        )

    def test_password_error(self):
        """Tests if a user has a provided a wrong password."""
        token = str((jwt.encode({
            "email": "bagendadeogracious@gmail.com"},
            settings.SECRET_KEY)).decode('utf-8')
        )
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.patch(
            self.change_password_url+"?token="+token,
            {"password": "bag"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         "password should be atleast 8 characters.")

    def test_successful_password_change(self):
        """Tests if a user has changed the password successfully."""
        token = str((jwt.encode(
            {"email": "bagendadeogracious@gmail.com"}, settings.SECRET_KEY)).decode('utf-8'))
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.patch(
            self.change_password_url+"?token="+token,
            {"password": "bagenda1234"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'],
            "you have reset your password successfully."
        )

    def test_wrong_token(self):
        """Tests if a user has provided a wrong token."""
        token = str((jwt.encode(
            {"email": "bagendadeogracious@gmail.com"},
            settings.SECRET_KEY)).decode('utf-8')
        )
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.patch(
            self.change_password_url+"?token="+token+"wrong",
            {"password": "bagenda1234"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         "verification link is invalid.")

    def test_password_change_provided(self):
        """Tests if a user has provided a password."""
        token = str((jwt.encode(
            {"email": "bagendadeogracious@gmail.com"}, 
            settings.SECRET_KEY)).decode('utf-8')
        )
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.patch(
            self.change_password_url+"?token="+token, {"pwd": "bagenda1234"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']
                         [0], "Password field is required.")

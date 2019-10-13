"""User registration tests."""
from .test_base import BaseTest
from rest_framework.views import status
from .test_data import (valid_user, empty_username,
                        invalid_user_email, short_password, missing_username_key,
                        invalid_username, invalid_password, empty_email, empty_password,
                        expired_token, invalid_token,
                        missing_username_key)


class UserRegistrationTest(BaseTest):
    """Contains user registration test methods."""

    def test_valid_registration(self):
        """Tests if a user can successfully create an account."""
        response = self.client.post(
            self.registration_url, valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "Bagzie12")

    def test_empty_username(self):
        """Tests if a user can not create an account without a username."""
        response = self.client.post(
            self.registration_url, empty_username, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['username'][0], "This field may not be blank.")

    def test_empty_email(self):
        """Tests if a user can not create an account without an email."""
        response = self.client.post(
            self.registration_url, empty_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['email'][0], "This field may not be blank.")

    def test_empty_password(self):
        """Tests if a user can not create an account without a password."""
        response = self.client.post(
            self.registration_url, empty_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['password'][0], "This field may not be blank.")

    def test_short_password(self):
        """Tests if a user can not create an account with a short password."""
        response = self.client.post(
            self.registration_url, short_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['password']
                         [0], "Password should be atleast 8 characters")

    def test_email_exists(self):
        """Tests if a user can not create an account with a taken email."""

        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.registration_url, valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['email'][0], "user with this email already exists.")

    def test_can_activate_a_user(self):
        """Tests if a user can be activated via token"""
        register_response = self.client.post(
            self.registration_url, valid_user, format='json')
        response = self.client.get(self.verify_url+"?token=" +
                                   register_response.data['token'], format='json')
        self.assertEqual(
            response.status_code,302)

    def test_user_cant_activate_with_expired_token(self):
        """Tests if a user cannot activate email with an invalid token."""
        response = self.client.get(
            self.verify_url+"?token="+expired_token, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_activate_with_invalid_token(self):
        """Tests if a user cannot activate email with an invalid token."""
        response = self.client.get(
            self.verify_url+"?token="+invalid_token, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """Tests if email entered by user is in the right format."""
        response = self.client.post(
            self.registration_url, invalid_user_email, format='json')
        data = response.json().get('errors')
        self.assertEqual(400, response.status_code)
        self.assertIn('Enter a valid email address.', data['email'][0])

    def test_register_same_username(self):
        """Tests to ensure the username entered is not already taken"""
        self.client.post(self.registration_url, valid_user, format='json')
        response = self.client.post(
            self.registration_url, valid_user, format='json')
        data = response.json().get('errors')
        self.assertEqual(response.status_code, 400)
        self.assertIn('user with this username already exists.',
                      data['username'])

    def test_register_invalid_username(self):
        """Tests if username entered by user is in the right format."""
        response = self.client.post(
            self.registration_url, invalid_username, format='json')
        data = response.json().get('errors')
        self.assertEqual(400, response.status_code)
        self.assertIn('The username is invalid please use letters and numbers',
                      data['error'])

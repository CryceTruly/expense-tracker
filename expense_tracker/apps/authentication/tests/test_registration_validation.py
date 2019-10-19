import json
import os

from django.test import TestCase
from django.urls import reverse

from .test_base import BaseTest
from .test_data import (valid_user, empty_username,
                        invalid_user_email, short_password, missing_username_key,
                        invalid_username, invalid_password, empty_email, empty_password,
                        expired_token, invalid_token,
                        missing_username_key, responses, same_email,
                        same_username)

class RegistrationValidationTest(BaseTest):

    def test_invalid_short_password(self):

        expected_response = responses['password_is_too_short']
        resp = self.client.post(
            self.registration_url, short_password, format='json')
        self.assertDictEqual(resp.data, expected_response)

    def test_signup_existing_email(self):

        expected_response = responses['email_already_exists']
        self.client.post(
            self.registration_url, valid_user, format='json')
        resp = self.client.post(
            self.registration_url, same_email, format='json')
        self.assertDictEqual(resp.data, expected_response)

    def test_signup_existing_username(self):
        expected_response = responses['username_already_exists']
        self.client.post(
            self.registration_url, valid_user, format='json')
        resp = self.client.post(
            self.registration_url, same_username, format='json')
        self.assertDictEqual(resp.data, expected_response)

    def test_signup_invalid_email(self):
        expected_response = responses['invalid_email']
        resp = self.client.post(
            self.registration_url, invalid_user_email, format='json')
        self.assertDictEqual(resp.data, expected_response)

import json
import os

from django.test import TestCase
from django.urls import reverse

from ..models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.username = 'sample12'
        self.email = 'sample@gmail.com'
        self.password = 'password'

    def test_user_creation(self):
        response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(response.get_full_name, 'sample12')

    def test_super_user_creation(self):
        response = User.objects.create_superuser(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
        self.assertEqual(response.get_full_name, 'sample12')

    def test_super_user_missing_password(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_superuser(username=self.username,
                                                     email=self.email,
                                                     password=None)

    def test_missing_email(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_user(username=self.username,
                                                email=None,
                                                password=self.password)

    def test_missing_username(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_user(username=None,
                                                email=self.email,
                                                password=self.password)

    def test_return_short_name(self):
        self.response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(self.response.get_short_name(), 'sample12')

    def test_str_return(self):
        self.response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(self.response.__str__(), 'sample@gmail.com')

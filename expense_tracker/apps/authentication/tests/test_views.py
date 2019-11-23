from .test_base import BaseTest
from .test_data import valid_user, invalid_user_email
from rest_framework import status


class TestRegister(BaseTest):
    def test_should_register_succesfuly(self):
        res = self.client.post(
            self.registration_url, data=valid_user, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_should_register_with_invalid_email(self):
        res = self.client.post(
            self.registration_url, data=invalid_user_email, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_register_with_a_taken_email(self):
        self.client.post(
            self.registration_url, data=valid_user, format='json')
        res = self.client.post(self.registration_url,
                               data=valid_user, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_get_user_profile(self):
        self.authenticate_user()
        res = self.client.get(
            self.viewusers, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

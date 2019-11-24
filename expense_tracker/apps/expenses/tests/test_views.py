from django.urls import reverse
from faker import Faker
import random
from expense_tracker.apps.authentication.models import User
from expense_tracker.apps.expenses.models import Expense
from rest_framework import status
import datetime
from expense_tracker.apps.authentication.tests.test_data import expired_token
from expense_tracker.apps.authentication.tests.test_base import BaseTest


class ViewTest(BaseTest):
    def setUp(self):
        self.expenses_url = reverse('expenses:expenses')
        self.fake = Faker()
        self.CATEGORY_OPTIONS = ['ONLINE_SERVICES',
                                 'RENT',
                                 'BUSINESS_MISCELLENOUS',
                                 'TRAVEL',
                                 'GENERAL_MERCHANDISE',
                                 'RESTUARANTS',
                                 'ENTERTAINMENT',
                                 'GASOLINE_FUEL',
                                 'INSURANCE',
                                 'OTHERS'
                                 ]
        self.expense = {
            'currency': str(self.fake.currency())[:5],
            'description': self.fake.sentence(),
            'name': self.fake.name(),
            'spent_on': self.fake.date(),
            'category': random.choice(self.CATEGORY_OPTIONS),
            'owner': User.objects.first(),
            'amount': self.fake.latitude()
        }
        self.expense_with_invalid_date = {
            'currency': str(self.fake.currency())[:5],
            'description': self.fake.sentence(),
            'name': self.fake.name(),
            'spent_on': datetime.date.today() + datetime.timedelta(days=1),
            'category': random.choice(self.CATEGORY_OPTIONS),
            'owner': User.objects.first(),
            'amount': self.fake.latitude()
        }
        self.updated_expense = {'name': 'Updated name',
                                'spent_on': datetime.date.today()}

    def authenticate_user_with_expired_token(self):
        user = User.objects.create_user(
            self.fake.email(), self.fake.email(), self.fake.password())
        user.is_verified = True
        user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + expired_token.replace(' ', ''))

    def create_expense(self):
        ex = Expense(currency=str(self.fake.currency())[:5],
                     description=self.fake.sentence(),
                     name=self.fake.name(),
                     spent_on=self.fake.date(),
                     category=random.choice(self.CATEGORY_OPTIONS),
                     owner=User.objects.first(),
                     amount=self.fake.latitude()
                     )
        ex.save()

    def test_should_not_add_expense_if_no_auth(self):
        response = self.client.post(self.expenses_url, format='json')
        self.assertEqual(
            str(response.data['detail']),
            'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_expense_correctly(self):
        self.authenticate_user()
        response = self.client.post(
            self.expenses_url, data=self.expense, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_not_create_expense_with_an_unverified_account(self):
        self.authenticate_user()
        user = User.objects.first()
        user.is_verified = False
        user.save()
        response = self.client.post(
            self.expenses_url, data=self.expense, format='json')
        self.assertEqual(str(
            response.data['detail']),
            'Your email is not verified, please check your email.')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_not_create_expense_with_an_expired_token(self):
        self.authenticate_user_with_expired_token()
        response = self.client.post(
            self.expenses_url, data=self.expense, format='json')
        self.assertEqual(str(
            response.data['detail']),
            'Your token is invalid, please login again.')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_not_create_expense_with_an_inactive_account(self):
        self.authenticate_user()
        user = User.objects.first()
        user.is_active = False
        user.save()
        response = self.client.post(
            self.expenses_url, data=self.expense, format='json')
        self.assertEqual(str(
            response.data['detail']),
            'Your account was deactivated, please contact admin.')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_not_create_expense_with_invalid_date(self):
        self.authenticate_user()
        response = self.client.post(
            self.expenses_url, data=self.expense_with_invalid_date,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_get_expenses_not_auth(self):
        response = self.client.get(self.expenses_url, format='json')
        self.assertEqual(
            str(response.data['detail']),
            'Authentication credentials were not provided.')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_should_get_own_expenses(self):
        self.authenticate_user()
        self.create_expense()
        res = self.client.get(self.expenses_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_render_expense_correctly(self):
        self.authenticate_user()
        self.create_expense()
        created_expense = Expense.objects.latest('id')
        res = self.client.get(reverse('expenses:expense',
                                      kwargs={'id': int(created_expense.id)}),
                              format='json')
        self.assertEqual(res.data['id'], created_expense.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_raise_an_error_when_expense_doesnot_exist(self):
        self.authenticate_user()
        self.create_expense()
        res = self.client.get(reverse('expenses:expense',
                                      kwargs={'id': int(3)}),
                              format='json')
        self.assertEqual(res.data['errors'], 'that expense was not found')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_update_expense_correctly(self):
        self.authenticate_user()
        self.create_expense()
        created_expense = Expense.objects.latest('id')
        res = self.client.patch(
            reverse('expenses:expense', kwargs={'id': created_expense.id}),
            data=self.updated_expense, format='json')
        self.assertEqual(res.data['data']['id'], created_expense.id)
        res2 = self.client.get(reverse('expenses:expense',
                                       kwargs={'id': created_expense.id}),
                               format='json')
        self.assertEqual(res2.data['id'], created_expense.id)
        self.assertEqual(res2.data['name'], 'Updated name')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_should_not_update_an_innexistent_expense(self):
        self.authenticate_user()
        self.create_expense()
        res = self.client.patch(
            reverse('expenses:expense', kwargs={'id': int(6)}),
            data=self.updated_expense, format='json')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_delete_an_expense(self):
        self.authenticate_user()
        self.create_expense()
        created_expense = Expense.objects.latest('id')
        res = self.client.delete(
            reverse('expenses:expense', kwargs={'id': created_expense.id}),
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_not_delete_an_innexisitent_expense(self):
        self.authenticate_user()
        self.create_expense()
        res = self.client.delete(
            reverse('expenses:expense', kwargs={'id': int(5)}), format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

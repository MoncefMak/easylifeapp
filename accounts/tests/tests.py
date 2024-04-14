from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.tests.factory import UserFactory
from companys.models import Company, CompanyBranch
from core.models import Country, City


class UserAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.client = APIClient()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_user(self):
        url = '/api/accounts/users/'
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_user(self):
        url = f'/api/accounts/users/{self.user.id}/'
        data = {'username': 'updateduser'}
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the user data has been updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'updateduser')

    def test_put_user(self):
        url = f'/api/accounts/users/{self.user.id}/'
        data = {'username': 'updateduser', 'email': 'updatenewuser@example.com'}
        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updatenewuser@example.com')

    def test_create_user_company_branch(self):
        country = Country.objects.create(name='Test Country', code='TC')
        city = City.objects.create(name='Test City', country=country, code='TC')
        url = '/api/accounts/create_user_company_branch/'
        data = {
            "user": {
                "username": "test_user_company",
                "email": "test_user_company@example.com",
                "password": "test_user_company_password",
            },
            "company": {
                'name': 'Test Company',
            },
            "branch": {
                'country': str(country.id),
                'city': str(city.id),
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(CompanyBranch.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)

    def test_login_user_email(self):
        url = '/api/accounts/login/'
        data = {
            'username': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_username(self):
        url = '/api/accounts/login/'
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        refresh_url = '/api/accounts/login/refresh/'
        access_token = self.get_access_token()['refresh']

        refresh_data = {'refresh': access_token}
        response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from companys.models import Company, CompanyBranch, CompanyBranchUserRelation
from companys.tests.factory import UserFactory, CountryFactory, CityFactory


class CompanyCreateAPIViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.second_user = UserFactory()
        self.country = CountryFactory()
        self.city = CityFactory(country=self.country)
        self.token = self.get_access_token(user=self.user)
        self.user.save()
        self.second_user.save()
        self.country.save()
        self.city.save()
        self.client = APIClient()


    def get_access_token(self, user):
        user.save()
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_company(self):
        url = '/api/companys/create/'
        data = {
            'name': 'Test Company',
            'branch': {
                'country': str(self.country.id),
                'city': str(self.city.id),
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(CompanyBranch.objects.count(), 1)
        company = Company.objects.first()
        branch = CompanyBranch.objects.first()
        self.assertEqual(company.name, 'Test Company')
        self.assertEqual(branch.name, 'Test Company')
        self.assertEqual(branch.country.name, 'Test Country')
        self.assertEqual(branch.city.name, 'Test City')
        self.assertTrue(branch.primary)

    def test_create_company_exist(self):
        Company.objects.create(name='Test Company', primary_user=self.user)
        url = '/api/companys/create/'
        data = {
            'name': 'Test Company',
            'branch': {
                'country': str(self.country.id),
                'city': str(self.city.id),
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], _('You already have an active company.'))

    def test_add_user_to_branch_company(self):
        company = Company.objects.create(name='Test Company', primary_user=self.user)
        branch = CompanyBranch.objects.create(name='Test Branch',
                                              company=company,
                                              country=self.country,
                                              city=self.city,
                                              primary=True)
        url = '/api/companys/add_user_company_branch/'
        data = {
            'branch': branch.pk,
            'user': self.second_user.id,
            'branch_permissions': [37, 38, 39, 40]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data, format='json', headers={'Branch-Company-Id': str(branch.pk)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user_in_branch_company(self):
        company = Company.objects.create(name='Test Company', primary_user=self.user)
        branch = CompanyBranch.objects.create(name='Test Branch',
                                              company=company,
                                              country=self.country,
                                              city=self.city,
                                              primary=True)
        branch_user_relation = CompanyBranchUserRelation.objects.create(user=self.second_user,
                                                                        branch=branch,
                                                                        created_by=self.user,
                                                                        updated_by=self.user)
        permission = Permission.objects.get(codename='change_companybranchuserrelation')
        branch_user_relation.branch_permissions.add(permission)
        url = f'/api/companys/update_user_company_branch/{branch_user_relation.id}/'
        data = {
            'branch': str(branch.id),
            'user': self.second_user.id,
            'branch_permissions': [37, 38, 39, 40]
        }
        headers = {'Branch-Company-Id': str(branch.pk)}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_access_token(user=self.second_user)}')
        response = self.client.patch(url, data, format='json', headers={'Branch-Company-Id': str(branch.pk)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_branch_relations(self):
        company = Company.objects.create(name='Test Company', primary_user=self.user)
        branch = CompanyBranch.objects.create(name='Test Branch',
                                              company=company,
                                              country=self.country,
                                              city=self.city,
                                              primary=True)
        url = '/api/companys/list_user_branch_relations/'
        headers = {'Branch-Company-ID': str(branch.id)}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_branch_relation(self):
        company = Company.objects.create(name='Test Company', primary_user=self.user)
        branch = CompanyBranch.objects.create(name='Test Branch',
                                              company=company,
                                              country=self.country,
                                              city=self.city,
                                              primary=True)
        branch_user_relation = CompanyBranchUserRelation.objects.create(user=self.second_user,
                                                                        branch=branch,
                                                                        created_by=self.user,
                                                                        updated_by=self.user)
        permission = Permission.objects.get(codename='change_companybranchuserrelation')
        branch_user_relation.branch_permissions.add(permission)
        url = '/api/companys/list_user_branch_relations/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_access_token(user=self.second_user)}')
        response = self.client.get(url, format='json', headers={'Branch-Company-ID': str(branch.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

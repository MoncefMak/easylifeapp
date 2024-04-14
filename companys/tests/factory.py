from factory import Factory, Faker, SubFactory

from accounts.models import User
from companys.models import Company, CompanyBranch, CompanyBranchUserRelation
from core.models import Country, City


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = 'password123'
    is_active = True


class CountryFactory(Factory):
    class Meta:
        model = Country

    name = 'Test Country'
    code = 'TC'


class CityFactory(Factory):
    class Meta:
        model = City

    name = 'Test City'
    country = SubFactory(CountryFactory)
    code = 'TC'



class CompanyFactory(Factory):
    class Meta:
        model = Company

    name = 'Test Company'
    primary_user = SubFactory(UserFactory)


class CompanyBranchFactory(Factory):
    class Meta:
        model = CompanyBranch

    name = 'Test Branch'
    company = SubFactory(CompanyFactory)
    country = SubFactory(CountryFactory)
    city = SubFactory(CityFactory)
    primary = True


class CompanyBranchUserRelationFactory(Factory):
    class Meta:
        model = CompanyBranchUserRelation

    user = SubFactory(UserFactory)
    branch = SubFactory(CompanyBranchFactory)
    created_by = SubFactory(UserFactory)
    updated_by = SubFactory(UserFactory)
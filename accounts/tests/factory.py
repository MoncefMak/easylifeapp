from factory import Factory, Faker, SubFactory

from accounts.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = 'password123'
    is_active = True

from django.db.models import UniqueConstraint, Q
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from companys.models import CompanyBranch
from core.abstract_class import AuditModel, TimeAuditModel, AuditActiveModel


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, is_active=False):
        if not email:
            raise ValueError("Enter an email.")
        if not username:
            raise ValueError("Please provide a username.")
        if not password:
            raise ValueError("A password is required.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=is_active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            is_active=True
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeAuditModel, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    mobile = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/avatar.png')
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE, blank=True, null=True)
    # Permissions
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['mobile'],
                name='unique_non_empty_mobile',
                condition=Q(mobile__isnull=False) & ~Q(mobile__exact=''),
                violation_error_message='هذا الرقم مستخدم من قبل'
            ),
        ]

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} {self.email}"


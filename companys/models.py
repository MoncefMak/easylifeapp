import uuid

from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext as _

from core.abstract_class import AuditActiveModel


class Company(AuditActiveModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    primary_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='companies')

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        constraints = [
            models.UniqueConstraint(fields=['name', 'is_active'],
                                    condition=models.Q(is_active=True),
                                    name='unique_active_company',
                                    violation_error_message=_('The Name of this Company already exists.')),
            models.UniqueConstraint(fields=['primary_user', 'is_active'],
                                    condition=models.Q(is_active=True),
                                    name='unique_active_primary_user',
                                    violation_error_message=_('There user have primary company already'))
        ]

    def __str__(self):
        return self.name

    def primary_branch(self):
        return self.branches.filter(primary=True).first()


class CompanyBranch(AuditActiveModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    country = models.ForeignKey("core.Country", on_delete=models.CASCADE)
    city = models.ForeignKey("core.City", on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'is_active', 'primary'],
                condition=models.Q(is_active=True, primary=True),
                name='unique_active_primary_company_branch',
                violation_error_message=_('There company have primary branch already')
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.company}"


class CompanyBranchUserRelation(AuditActiveModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name='user_relations')
    branch_permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return f"{self.user} - {self.branch} - {self.branch_permissions.all()}"

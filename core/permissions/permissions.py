from django.shortcuts import get_object_or_404
from rest_framework import permissions

from companys.models import CompanyBranch, CompanyBranchUserRelation

import logging


class CompanyPermissions(permissions.BasePermission):
    def __init__(self, codename):
        self.codename = codename
        super().__init__()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            branch_company_id = request.headers.get('Branch-Company-Id')
            if not branch_company_id:
                print("Branch-Company-Id header is missing")
                raise KeyError("Branch-Company-Id header is missing")
        except KeyError as e:
            return False
        company_branch = get_object_or_404(CompanyBranch, id=branch_company_id)
        user = request.user
        if user == company_branch.company.primary_user:
            return True
        else:
            try:
                relation = CompanyBranchUserRelation.objects.get(user=user, branch=company_branch, is_active=True)
                if relation.branch_permissions.filter(codename=self.codename).exists():
                    return True
            except CompanyBranchUserRelation.DoesNotExist:
                pass  # User does not have any relation with this branch
        return False

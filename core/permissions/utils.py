from core.permissions.permissions import CompanyPermissions


def company_primary_permission_factory(codename):
    class CompanyPrimaryPermissionsWithCodename(CompanyPermissions):
        def __init__(self):
            super().__init__(codename)
    return CompanyPrimaryPermissionsWithCodename

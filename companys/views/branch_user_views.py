from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView

from companys.models import CompanyBranchUserRelation
from companys.serlizers.baranch_user_serializers import CompanyBranchUserRelationSerializer
from core.permissions.utils import company_primary_permission_factory


class AddUserToBranchCompany(CreateAPIView):
    queryset = CompanyBranchUserRelation.objects.all().order_by('id')
    serializer_class = CompanyBranchUserRelationSerializer
    permission_classes = [company_primary_permission_factory('add_companybranchuserrelation')]

    def get_serializer_context(self):
        return {"headers": self.request.headers}


class UpdateUserInBranchCompany(UpdateAPIView):
    queryset = CompanyBranchUserRelation.objects.all().order_by('id')
    serializer_class = CompanyBranchUserRelationSerializer
    permission_classes = [company_primary_permission_factory('change_companybranchuserrelation')]

    def get_serializer_context(self):
        return {"headers": self.request.headers}


class ListUserBranchRelations(ListAPIView):
    serializer_class = CompanyBranchUserRelationSerializer
    permission_classes = [company_primary_permission_factory('view_companybranchuserrelation')]

    def get_queryset(self):
        branch_id = self.request.headers.get('Branch-Company-ID')
        return CompanyBranchUserRelation.objects.filter(branch__id=branch_id, is_active=True).order_by('id')

    def get_serializer_context(self):
        return {"headers": self.request.headers}

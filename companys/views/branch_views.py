from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from companys.models import CompanyBranch
from companys.serlizers.company_serializers import CompanyBranchSerializer


class BranchCreate(CreateAPIView):
    model = CompanyBranch.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyBranchSerializer

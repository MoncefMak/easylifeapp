from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from companys.models import Company
from companys.serlizers.company_serializers import CompanyBranchSerializer, CompanySerializer


class CompanyWithBranchCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        if Company.objects.filter(primary_user=request.user, is_active=True).exists():
            return Response({'error': _('You already have an active company.')}, status=status.HTTP_400_BAD_REQUEST)

        company_serializer = CompanySerializer(data=request.data)
        branch_serializer = CompanyBranchSerializer(data=request.data.get('branch'))

        if company_serializer.is_valid() and branch_serializer.is_valid():
            company = company_serializer.save(primary_user=request.user, created_by=request.user)
            branch_serializer.save(name=company.name, company=company, created_by=request.user)
            return Response(company_serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'company_errors': company_serializer.errors,
            'branch_errors': branch_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

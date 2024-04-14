from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext as _

from accounts.models import User
from accounts.permissions import UserPermissions
from accounts.serializers import UserSerializer, UserUpdateSerializer, LogInSerializer
from companys.serlizers.company_serializers import CompanySerializer, CompanyBranchSerializer


class UserCreateRetrieveUpdateAPIView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    serializer_update_class = UserUpdateSerializer
    permission_classes = [UserPermissions]

    def get_queryset(self):
        if self.request.method in ['PATCH', 'PUT']:
            return User.objects.all()
        return User.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return self.serializer_update_class
        return self.serializer_class


class UserCompanyWithBranchCreate(APIView):
    def post(self, request, format=None):
        user_data = request.data.get('user')
        company_data = request.data.get('company')
        branch_data = request.data.get('branch')

        with transaction.atomic():
            user_serializer = UserSerializer(data=user_data)
            if not user_serializer.is_valid():
                return Response({'user_errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            company_serializer = CompanySerializer(data=company_data)
            if not company_serializer.is_valid():
                return Response({'company_errors': company_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            branch_serializer = CompanyBranchSerializer(data=branch_data)
            if not branch_serializer.is_valid():
                return Response({'branch_errors': branch_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            user_instance = user_serializer.save(password=user_data.get('password'))
            company_instance = company_serializer.save(primary_user=user_instance, created_by=user_instance)
            branch_serializer.save(name=company_instance.name, company=company_instance, created_by=user_instance)
        return Response(company_serializer.data, status=status.HTTP_201_CREATED)





class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer

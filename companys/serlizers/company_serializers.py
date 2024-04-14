from rest_framework import serializers

from companys.models import Company, CompanyBranch


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanyBranchSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = CompanyBranch
        fields = ['id', 'name', 'company', 'country', 'city', 'is_active']

    def create(self, validated_data):
        validated_data.setdefault('primary', True)
        return super().create(validated_data)

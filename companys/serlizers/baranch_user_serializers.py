from rest_framework import serializers

from companys.models import CompanyBranchUserRelation


class CompanyBranchUserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranchUserRelation
        fields = ["id", "user", "branch", "branch_permissions"]



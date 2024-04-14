from django.contrib import admin

from companys.models import Company, CompanyBranch, CompanyBranchUserRelation


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'primary_user__username']


@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "city", "company", "primary"]
    list_filter = ["company", "country", "city"]
    search_fields = ['name', 'company__name', 'country__name', 'city__name']
    autocomplete_fields = ['company']


@admin.register(CompanyBranchUserRelation)
class CompanyBranchUserRelationAdmin(admin.ModelAdmin):
    filter_horizontal = ("branch_permissions",)

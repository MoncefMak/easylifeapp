from django.urls import path

from companys.views.branch_user_views import AddUserToBranchCompany, UpdateUserInBranchCompany, ListUserBranchRelations
from companys.views.company_views import CompanyWithBranchCreate

urlpatterns = [
    path('create/', CompanyWithBranchCreate.as_view()),
    path('add_user_company_branch/', AddUserToBranchCompany.as_view()),
    path('update_user_company_branch/<int:pk>/', UpdateUserInBranchCompany.as_view()),
    path('list_user_branch_relations/', ListUserBranchRelations.as_view()),
]

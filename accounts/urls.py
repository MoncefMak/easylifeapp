from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # new

from accounts.views import LogInView, UserCreateRetrieveUpdateAPIView, UserCompanyWithBranchCreate

urlpatterns = [
    path('users/', UserCreateRetrieveUpdateAPIView.as_view()),
    path('users/<int:pk>/', UserCreateRetrieveUpdateAPIView.as_view()),
    path('create_user_company_branch/', UserCompanyWithBranchCreate.as_view()),
    path('login/', LogInView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
]

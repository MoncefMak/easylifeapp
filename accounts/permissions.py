from rest_framework import permissions


class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_authenticated:
            return obj == request.user
        return False

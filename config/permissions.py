from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_owner == request.user


class AllowAny(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_public

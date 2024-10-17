from rest_framework.permissions import BasePermission, SAFE_METHODS

from crm.models import ADMIN


class IsAuth(BasePermission):
    message = "Ro'yxatdan o'tish talab qilinadi"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == ADMIN
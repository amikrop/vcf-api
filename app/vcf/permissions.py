from django.conf import settings
from rest_framework import permissions


class IsAuthorizedOrReadOnly(permissions.BasePermission):
    """Allows read-only access for everyone.
    Write methods require: Authorization: Bearer <settings.WRITE_TOKEN>
    """

    def has_permission(self, request, view):
        # Always allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Enforce token on write methods
        auth_header = request.headers.get("Authorization", "")
        expected = f"Bearer {settings.WRITE_TOKEN}"
        return auth_header == expected

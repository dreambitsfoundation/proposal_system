from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated

class UserViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return not isinstance(request.user, AnonymousUser)
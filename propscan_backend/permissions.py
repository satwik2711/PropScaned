from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class IsTokenVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        authentication = JWTAuthentication()
        try:
            authentication.authenticate(request)
        except InvalidToken:
            return False
        else:
            return True

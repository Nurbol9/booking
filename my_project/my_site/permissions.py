from rest_framework.permissions import BasePermission


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client' :
            return True
        return False



class OwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'
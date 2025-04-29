from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow access to admins.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Admin').exists()

class IsShopAdmin(BasePermission):
    """
    Custom permission to only allow access to shop admins.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='ShopAdmin').exists()


class IsCustomer(BasePermission):
    """
    Custom permission to only allow access to customers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Customer').exists()

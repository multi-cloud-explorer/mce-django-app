from rest_framework import permissions

from mce_django_app import perms

class CompanyPermissions(perms.CompanyPermissions, permissions.BasePermission):
    pass


class TagPermissions(perms.TagPermissions, permissions.BasePermission):
    pass


class UserPermissions(perms.UserPermissions, permissions.BasePermission):
    pass


class ResourcePermissions(perms.ResourcePermissions, permissions.BasePermission):
    pass


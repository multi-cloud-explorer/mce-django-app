from rest_framework import permissions
from mce_django_app.constants import UserRole

class MCEPermissions(permissions.BasePermission):
    GET = []
    HEAD = []
    OPTIONS = []
    POST = []
    PUT = []
    PATCH = []
    DELETE = []

    def has_permission(self, request, view):

        REQUIRED_ROLES = getattr(self, request.method, [])

        result = bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            getattr(request.user, 'role', None) in REQUIRED_ROLES or
            request.user.is_superuser
        )

        # print('!!! path              : ', request.path)
        # print('!!! content_type      : ', request.content_type)
        # print('!!! method            : ', request.method)
        # print('!!! REQUIRED_ROLES    : ', REQUIRED_ROLES)
        # print('!!! request.user.role : ', getattr(request.user, 'role', None))
        # print('!!! is_superuser      : ', request.user.is_superuser)
        # print('!!! RESULT            : ', result)

        return result

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # print('!!!!!!!! : has_object_permission...')
        return True


class CompanyPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = []
    PUT = []
    PATCH = [UserRole.OWNER]
    DELETE = []


class TagPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = [UserRole.OWNER]
    PUT = [UserRole.OWNER]
    PATCH = [UserRole.OWNER]
    DELETE = [UserRole.OWNER]


class UserPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER]
    HEAD = [UserRole.OWNER, UserRole.USER]
    OPTIONS = [UserRole.OWNER, UserRole.USER]
    POST = [UserRole.OWNER]
    PUT = []
    PATCH = [UserRole.OWNER, UserRole.USER]
    DELETE = [UserRole.OWNER, UserRole.USER]

    def has_object_permission(self, request, view, obj):
        if request.user.is_owner:
            return True
        return request.user.pk == obj.pk


class ResourcePermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = [UserRole.OWNER, UserRole.SERVICE]
    PUT = [UserRole.OWNER]
    PATCH = [UserRole.OWNER, UserRole.SERVICE]
    DELETE = [UserRole.OWNER, UserRole.SERVICE]

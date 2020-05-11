
# TODO: Token
# TODO: ResourceEventChange

from mce_django_app.constants import UserRole

class MCEPermissions:
    GET = []
    HEAD = []
    OPTIONS = []
    POST = []
    PUT = []
    PATCH = []
    DELETE = []

    def has_permission(self, request, view=None, method=None):

        REQUIRED_ROLES = getattr(self, method or request.method, [])

        result = bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            not request.user.is_anonymous and
            getattr(request.user, 'role', None) in REQUIRED_ROLES or
            request.user.is_superuser
        )

        # print("!!! has_permission : ", request.user, getattr(request.user, 'role', None), REQUIRED_ROLES, method or request.method, result)

        return result

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


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


class ProviderPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = []
    PUT = []
    PATCH = []
    DELETE = []


class RegionPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = []
    PUT = []
    PATCH = []
    DELETE = []


class ResourceTypePermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = []
    PUT = []
    PATCH = []
    DELETE = []


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


class ResourcePermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = [UserRole.OWNER, UserRole.SERVICE]
    PUT = []
    PATCH = [UserRole.OWNER, UserRole.SERVICE]
    DELETE = [UserRole.OWNER, UserRole.SERVICE]


class BaseSubscriptionPermissions(MCEPermissions):

    GET = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    HEAD = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    OPTIONS = [UserRole.OWNER, UserRole.USER, UserRole.SERVICE]
    POST = [UserRole.OWNER]
    PUT = []
    PATCH = [UserRole.OWNER]
    DELETE = [UserRole.OWNER]


class SubscriptionAzurePermissions(BaseSubscriptionPermissions):
    pass


class ResourceAzurePermissions(ResourcePermissions):
    pass


class SubscriptionAWSPermissions(BaseSubscriptionPermissions):
    pass


class ResourceAWSPermissions(ResourcePermissions):
    pass


class ProjectGCPPermissions(BaseSubscriptionPermissions):
    pass


class ResourceGCPPermissions(ResourcePermissions):
    pass


class VcenterPermissions(BaseSubscriptionPermissions):
    pass


class DatacenterVMwarePermissions(ResourcePermissions):
    pass


class ResourceVMwarePermissions(ResourcePermissions):
    pass

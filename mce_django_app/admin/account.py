from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token

from mce_django_app import perms
from .common import BaseModelAdmin, BaseModelAdminWithCompanyFieldMixin

USER_MODEL = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(Token)


@admin.register(USER_MODEL)
class UserAdmin(BaseModelAdminWithCompanyFieldMixin, BaseModelAdmin, UserAdmin):
    PERMS = perms.UserPermissions
    fieldsets = (
        (None, {'fields': ('company', 'username', 'password', 'role')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    pass

@admin.register(Token)
class TokenAdmin(BaseModelAdmin):
    pass


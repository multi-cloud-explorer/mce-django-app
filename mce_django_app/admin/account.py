from django.contrib.auth.models import Group, User
from django.contrib import admin
from django.contrib.auth import get_user_model

#from organizations.models import (Organization, OrganizationUser, OrganizationOwner)
from rest_framework.authtoken.models import Token

from mce_django_app.admin.common import BaseModelAdmin

USER_MODEL = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(Token)
# admin.site.unregister(Organization)
# admin.site.unregister(OrganizationUser)
# admin.site.unregister(OrganizationOwner)

@admin.register(USER_MODEL)
class UserAdmin(BaseModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    pass


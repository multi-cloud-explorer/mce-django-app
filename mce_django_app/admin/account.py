from django.contrib.auth.models import Group, User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import account as models
from mce_django_app.admin.common import BaseModelAdmin

try:
    admin.site.unregister(Group)
    admin.site.unregister(User)
except:
    pass

@admin.register(models.User)
class UserAdmin(BaseModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    pass


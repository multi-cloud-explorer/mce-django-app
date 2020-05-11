from django.contrib import admin

from mce_django_app import perms
from mce_django_app.models import gcp as models
from .base import BaseModelAdmin, ReadOnlyModelAdminMixIn, BaseModelAdminWithCompanyFieldMixin

@admin.register(models.ProjectGCP)
class ProjectGCPAdmin(BaseModelAdminWithCompanyFieldMixin, BaseModelAdmin):
    list_display = (
        #'id',
        # 'created',
        # 'updated',
        'project_id',
        # 'credentials',
        # 'username',
        # 'password',
        # 'assume_role',
    )
    list_filter = ('created', 'updated')


@admin.register(models.ResourceGCP)
class ResourceGCPAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    list_display = (
        #'id',
        # 'created',
        # 'updated',
        'resource_id',
        # 'slug',
        'name',
        # 'provider',
        'resource_type',
        'company',
        # 'metas',
        # 'locked',
        # 'active',
        'project',
    )
    list_filter = (
        # 'created',
        # 'updated',
        # 'provider',
        # 'resource_type',
        'company',
        # 'locked',
        # 'active',
        'project',
    )
    search_fields = ('slug', 'name')
    prepopulated_fields = {'slug': ['name']}

# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ProjectGCP, ResourceGCP


@admin.register(ProjectGCP)
class ProjectGCPAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'project_id',
        'credentials',
        'username',
        'password',
        'assume_role',
    )
    list_filter = ('created', 'updated')


@admin.register(ResourceGCP)
class ResourceGCPAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'resource_id',
        'slug',
        'name',
        'provider',
        'resource_type',
        'company',
        'metas',
        'locked',
        'active',
        'project',
    )
    list_filter = (
        'created',
        'updated',
        'provider',
        'resource_type',
        'company',
        'locked',
        'active',
        'project',
    )
    search_fields = ('slug', 'name')
    prepopulated_fields = {'slug': ['name']}

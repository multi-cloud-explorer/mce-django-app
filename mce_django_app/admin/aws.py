# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import SubscriptionAWS, ResourceAWS


@admin.register(SubscriptionAWS)
class SubscriptionAWSAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'subscription_id',
        'name',
        'company',
        'provider',
        'active',
        'default_region',
        'username',
        'password',
        'assume_role',
    )
    list_filter = ('created', 'updated', 'company', 'provider', 'active')
    search_fields = ('name',)


@admin.register(ResourceAWS)
class ResourceAWSAdmin(admin.ModelAdmin):
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
        'subscription',
    )
    list_filter = (
        'created',
        'updated',
        'provider',
        'resource_type',
        'company',
        'locked',
        'active',
        'subscription',
    )
    search_fields = ('slug', 'name')
    prepopulated_fields = {'slug': ['name']}

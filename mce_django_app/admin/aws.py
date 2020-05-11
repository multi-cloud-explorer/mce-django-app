# -*- coding: utf-8 -*-
from django.contrib import admin

from mce_django_app import perms
from mce_django_app.models import aws as models
from .base import BaseModelAdmin, ReadOnlyModelAdminMixIn, BaseModelAdminWithCompanyFieldMixin


@admin.register(models.SubscriptionAWS)
class SubscriptionAWSAdmin(BaseModelAdminWithCompanyFieldMixin, BaseModelAdmin):
    PERMS = perms.SubscriptionAWSPermissions
    list_display = ['subscription_id', 'name', 'company_name']
    list_filter = ['company__name']
    search_fields = ['name']
    list_select_related = ['company', 'provider']


@admin.register(models.ResourceAWS)
class ResourceAWSAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.ResourceAWSPermissions
    list_display = [
        'name',
        'resource_type_name',  # TODO: faire lien html vers le type
        'company_name',
        'subscription_name',
        'region_name',
    ]
    list_filter = [
        'company__name',
        'region__name',
        'subscription__name',
        'subscription__subscription_id',
    ]
    list_select_related = [
        'resource_type',
        'company',
        'subscription',
        'region'
    ]
    search_fields = ('slug', 'name')
    prepopulated_fields = {'slug': ['name']}

from django.contrib import admin

from mce_django_app import perms
from mce_django_app.models import azure as models
from .base import BaseModelAdmin, ReadOnlyModelAdminMixIn, BaseModelAdminWithCompanyFieldMixin


@admin.register(models.SubscriptionAzure)
class SubscriptionAzureAdmin(BaseModelAdminWithCompanyFieldMixin, BaseModelAdmin):
    PERMS = perms.SubscriptionAzurePermissions
    list_display = ('subscription_id', 'name', 'company_name', 'tenant')
    search_fields = ['subscription_id', 'name']
    list_filter = ['company__name', 'tenant']
    #sortable_by = ['name', 'location', 'tenant']
    #autocomplete_fields = ['account']
    list_select_related = ['company', 'provider']


@admin.register(models.ResourceAzure)
class ResourceAzureAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.ResourceAzurePermissions
    list_display = (
        'name',
        'resource_type_name', # TODO: faire lien html vers le type
        'resource_group_name',
        'company_name',
        'subscription_name',
        'region_name',
    )
    search_fields = ['resource_id', 'name', 'resource_type__name']

    list_filter = [
        'company__name',
        'region__name',
        'subscription__name', 
        'subscription__tenant',
        'subscription__subscription_id',
        #'resource_type__name',
        #'resource_group__name'
    ]

    list_select_related = [
        'resource_type',
        'company',
        'resource_group',
        'subscription',
        'region'
    ]



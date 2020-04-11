from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import azure as models
from mce_django_app.admin.common import resource_type_name


def subscription_name(obj):
    subscription = obj.subscription
    return f"{subscription.name} ({subscription.pk})"


subscription_name.short_description = _('Subscription')


def tenant_name(obj):
    return obj.subscription.tenant


tenant_name.short_description = _('Tenant')


def resource_group_name(obj):
    return obj.resource_group.name


resource_group_name.short_description = _('Resource Group')


class SubscriptionAzureAdmin(ModelAdmin):
    list_display = ('id', 'name', 'location', 'tenant')
    search_fields = ['id', 'name']
    list_filter = ['location', 'tenant']
    sortable_by = ['name', 'location', 'tenant']
    autocomplete_fields = ['account']


class ResourceGroupAzureAdmin(ModelAdmin):
    list_display = ('name', tenant_name, subscription_name, 'location')
    search_fields = ['id', 'name']
    list_filter = ['subscription__name', 'subscription__id', 'location']
    sortable_by = ['name']


class ResourceAzureAdmin(ModelAdmin):
    list_display = (
        'name',
        resource_type_name,
        resource_group_name,
        tenant_name,
        subscription_name,
        'location',
    )
    search_fields = ['id', 'name']
    list_filter = [
        'location',
        'subscription__name',
        'subscription__id',
        'resource_group__name',
    ]
    sortable_by = ['name']
    # exclude = ('birth_date',)


admin.site.register(models.Subscription, SubscriptionAzureAdmin)
admin.site.register(models.ResourceGroupAzure, ResourceGroupAzureAdmin)
admin.site.register(models.ResourceAzure, ResourceAzureAdmin)

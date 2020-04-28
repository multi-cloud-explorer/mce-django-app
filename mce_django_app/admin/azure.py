from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from mce_django_app.models import azure as models
from mce_django_app.admin.common import BaseModelAdmin, ReadOnlyModelAdminMixIn

#
# def subscription_name(obj):
#     subscription = obj.subscription
#     return f"{subscription.name} ({subscription.subscription_id})"
# subscription_name.short_description = _('Souscription')
# subscription_name.admin_order_field = 'subscription__name'
#

# def tenant_name(obj):
#     return obj.subscription.tenant
# tenant_name.short_description = _('Locataire')
# tenant_name.admin_order_field = 'tenant'


# def resource_group_name(obj):
#     return obj.resource_group.name
# resource_group_name.short_description = _('Groupe de Ressource')
#

@admin.register(models.SubscriptionAzure)
class SubscriptionAzureAdmin(BaseModelAdmin):
    list_display = ('subscription_id', 'name', 'company_name', 'location', 'tenant')
    search_fields = ['subscription_id', 'name']
    list_filter = ['company__name', 'location', 'tenant']
    #sortable_by = ['name', 'location', 'tenant']
    #autocomplete_fields = ['account']
    list_select_related = ['company']


# @admin.register(models.ResourceGroupAzure)
# class ResourceGroupAzureAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
#
#     list_display = ('name', company_name, tenant_name, subscription_name, 'location', 'resource_count')
#     search_fields = ['resource_id', 'name']
#     list_filter = ['company__name', 'subscription__name', 'subscription__subscription_id', 'location']
#     list_select_related = ['resource_type', 'company', 'subscription']
#
#     def resource_count(self, obj):
#         return obj.resourceazure_set.count()
#         #return obj._resource_count
#     resource_count.short_description = _('Resources')


@admin.register(models.ResourceAzure)
class ResourceAzureAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):

    list_display = (
        'name',
        'resource_type_name', # TODO: faire lien html vers le type
        'resource_group_name',
        'company_name',
        'tenant',
        'subscription_name',
        'location',
    )
    search_fields = ['resource_id', 'name']
    list_filter = [
        'company__name',
        'location', 
        'subscription__name', 
        'subscription__subscription_id', 
        'resource_group__name'
    ]
    list_select_related = ['resource_type', 'company', 'resource_group', 'subscription']



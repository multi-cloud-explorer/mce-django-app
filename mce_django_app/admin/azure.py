from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import azure as models
from mce_django_app.admin.common import resource_type_name


def subscription_name(obj):
    subscription = obj.subscription
    return f"{subscription.name} ({subscription.pk})"
subscription_name.short_description = _('Souscription')
subscription_name.admin_order_field = 'subscription'


def tenant_name(obj):
    return obj.subscription.tenant
tenant_name.short_description = _('Locataire')
tenant_name.admin_order_field = 'tenant'


def resource_group_name(obj):
    return obj.resource_group.name
resource_group_name.short_description = _('Groupe de Ressource')


class SubscriptionAzureAdmin(ModelAdmin):
    list_display = ('subscription_id', 'name', 'location', 'tenant')
    search_fields = ['subscription_id', 'name']
    list_filter = ['location', 'tenant']
    sortable_by = ['name', 'location', 'tenant']
    autocomplete_fields = ['account']
    list_select_related = ['company', 'account']

"""
class SubscriptionNameFilter(admin.SimpleListFilter):
    title = _("Subscription Name")
    parameter_name = "subscription"
    field_path = "subscription__name"
"""

class ResourceGroupAzureAdmin(ModelAdmin):
    list_display = ('name', tenant_name, subscription_name, 'location')
    search_fields = ['resource_id', 'name']
    list_filter = ['subscription__name', 'subscription__subscription_id', 'location']
    sortable_by = ['name']
    list_select_related = ['resource_type', 'company', 'subscription']

class ResourceAzureAdmin(ModelAdmin):
    list_display = (
        'name',
        resource_type_name, # TODO: faire lien html vers le type
        resource_group_name,
        tenant_name,
        subscription_name,
        'location',
    )
    search_fields = ['resource_id', 'name']
    list_filter = [
        'location', 
        'subscription__name', 
        'subscription__subscription_id', 
        'resource_group__name'
    ]
    """
    TODO:
    list_filter = [
        #('location', admin.SimpleListFilter),
        ('subscription__name', SubscriptionNameFilter),
        #('subscription__id', admin.SimpleListFilter),
        #('resource_group__name', admin.SimpleListFilter),
    ]
    """
    sortable_by = ['name', 'subscription']
    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True
    list_select_related = ['resource_type', 'company', 'resource_group', 'subscription']


admin.site.register(models.Subscription, SubscriptionAzureAdmin)
admin.site.register(models.ResourceGroupAzure, ResourceGroupAzureAdmin)
admin.site.register(models.ResourceAzure, ResourceAzureAdmin)

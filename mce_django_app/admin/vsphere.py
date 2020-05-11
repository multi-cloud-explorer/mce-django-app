from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from mce_django_app.models import vsphere as models
from mce_django_app.admin.common import BaseModelAdmin, ReadOnlyModelAdminMixIn

@admin.register(models.Vcenter)
class VcenterAdmin(BaseModelAdmin):

    list_display = ('name', 'company_name')
    # search_fields = ['subscription_id', 'name']
    # list_filter = ['company__name', 'location', 'tenant']
    # #sortable_by = ['name', 'location', 'tenant']
    # #autocomplete_fields = ['account']
    list_select_related = ['company']

@admin.register(models.DatacenterVMware)
class DatacenterVMwareAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):

    list_display = (
        'name',
        'resource_type_name',
        'company_name',
        'vcenter_name'
    )

    search_fields = ['resource_id', 'name']
    list_filter = [
        'company__name',
        'vcenter__name',
    ]
    list_select_related = ['resource_type', 'company', 'vcenter']

@admin.register(models.ResourceVMware)
class ResourceVMwareAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):

    list_display = (
        'name',
        'resource_type_name',
        'company_name',
        'datacenter_name'
    )
    search_fields = ['resource_id', 'name']
    list_filter = [
        'company__name',
        'datacenter__name',
    ]
    list_select_related = ['resource_type', 'company', 'datacenter']






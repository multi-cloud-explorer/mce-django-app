from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import common as models

# from .. import forms


def resource_type_name(obj):
    return obj.resource_type.name
resource_type_name.short_description = _('Type de Resource')

def company_name(obj):
    return obj.company.name
company_name.short_description = _('Société')

class ResourceEventChangeAdmin(ModelAdmin):
    list_display = ('object_id', 'content_type', 'action')
    list_filter = ['action']


class GenericAccountAdmin(ModelAdmin):
    list_display = ('name', 'description', 'username')
    search_fields = ['name']
    sortable_by = ['name', 'username']


class CompanyAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    sortable_by = ['name']


class TagAdmin(ModelAdmin):
    list_display = ('name', 'value', 'provider')
    search_fields = ['name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider', 'value']
    # autocomplete_fields = ['provider']


class ResourceTypeAdmin(ModelAdmin):
    list_display = ('name', 'description', 'provider')
    search_fields = ['name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider']
    # autocomplete_fields = ['provider']
    # formfield_overrides = {
    #    models.TextField: {'provider': Select2TagWidget},
    # }


class ResourceAdmin(ModelAdmin):
    list_display = ('name', resource_type_name, 'provider', company_name)
    search_fields = ['resource_id', 'name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider']
    autocomplete_fields = ['resource_type']  # , 'provider']
    list_select_related = ['company', 'resource_type']


admin.site.register(models.ResourceEventChange, ResourceEventChangeAdmin)
admin.site.register(models.GenericAccount, GenericAccountAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.ResourceType, ResourceTypeAdmin)
admin.site.register(models.Resource, ResourceAdmin)

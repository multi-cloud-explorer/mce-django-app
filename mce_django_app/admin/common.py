from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import common as models

# from .. import forms


def resource_type_name(obj):
    return obj.resource_type.name


resource_type_name.short_description = _('Resource Type')


class ResourceEventChangeAdmin(ModelAdmin):
    list_display = ('object_id', 'content_type', 'action')
    list_filter = ['action']


class GenericAccountAdmin(ModelAdmin):
    list_display = ('name', 'description', 'username')
    search_fields = ['name']
    sortable_by = ['name', 'username']


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
    list_display = ('name', resource_type_name, 'provider')
    search_fields = ['id', 'name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider']
    autocomplete_fields = ['resource_type']  # , 'provider']


admin.site.register(models.ResourceEventChange, ResourceEventChangeAdmin)
admin.site.register(models.GenericAccount, GenericAccountAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.ResourceType, ResourceTypeAdmin)
admin.site.register(models.Resource, ResourceAdmin)

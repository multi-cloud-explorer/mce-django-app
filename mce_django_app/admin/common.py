from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mce_django_app.models import common as models

"""
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class Admin:
    actions = [make_published]
"""

# locked
"""
<i class="material-icons green-color medium-icon">check_circle</i>
<i class="material-icons red-color medium-icon">highlight_off</i>
def html_active(obj):
    return format_html(_html)
html_asset_task_state.short_description = _('State')
"""

def resource_type_name(obj):
    return obj.resource_type.name
resource_type_name.short_description = _('Type de Resource')

def company_name(obj):
    return obj.company.name
company_name.short_description = _('Société')


class BaseModelAdmin(ModelAdmin):
    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True
    view_on_site = True
    #actions_on_top = True
    #actions_on_bottom = True
    show_full_result_count = False # perfs
    exclude = ['is_removed']

class ReadOnlyModelAdminMixIn:

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.ResourceEventChange)
class ResourceEventChangeAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
    date_hierarchy = 'created'
    list_display = ('object_id', '__str__', 'action', 'created')
    list_filter = ['action']
    list_select_related = ['content_type']
    readonly_fields = ['object_id', 'content_type', 'action', 'created']


@admin.register(models.GenericAccount)
class GenericAccountAdmin(BaseModelAdmin):
    list_display = ('name', 'description', 'username')
    search_fields = ['name']
    #sortable_by = ['name', 'username']


@admin.register(models.Company)
class CompanyAdmin(BaseModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    sortable_by = ['name']


@admin.register(models.Tag)
class TagAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
    list_display = ('name', 'value', 'provider')
    search_fields = ['name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider', 'value']
    # autocomplete_fields = ['provider']


@admin.register(models.ResourceType)
class ResourceTypeAdmin(BaseModelAdmin):
    list_display = ('name', 'description', 'provider')
    search_fields = ['name']
    list_filter = ['provider']
    sortable_by = ['name', 'provider']
    # autocomplete_fields = ['provider']
    # formfield_overrides = {
    #    models.TextField: {'provider': Select2TagWidget},
    # }


@admin.register(models.Resource)
class ResourceAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
    list_display = ('name', resource_type_name, 'provider', company_name, 'active', 'locked')
    search_fields = ['resource_id', 'name']
    list_filter = [
        ('company_name', admin.RelatedOnlyFieldListFilter),
        #'provider', 
        ('active', admin.BooleanFieldListFilter), 
        #'locked'
    ]
    sortable_by = ['name', 'provider']
    autocomplete_fields = ['resource_type']  # , 'provider']
    list_select_related = ['company', 'resource_type']
    #list_editable = ['active', 'locked']


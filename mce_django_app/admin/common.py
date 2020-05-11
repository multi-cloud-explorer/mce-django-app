from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from daterangefilter.filters import PastDateRangeFilter

from mce_django_app.models import common as models
from mce_django_app import perms

from .base import ReadOnlyModelAdminMixIn, BaseModelAdmin, BaseModelAdminWithCompanyFieldMixin

@admin.register(models.Provider)
class ProviderAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.ProviderPermissions
    list_display = ['name']


@admin.register(models.Region)
class RegionAdmin(ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.RegionPermissions
    list_display = ['provider', 'name']


@admin.register(models.ResourceType)
class ResourceTypeAdmin(BaseModelAdmin):
    PERMS = perms.ResourceTypePermissions
    list_display = ('name', 'description', 'provider_name', 'exclude_sync')
    search_fields = ['name']
    list_filter = ['provider', 'exclude_sync']
    sortable_by = ['name', 'provider']
    # autocomplete_fields = ['provider']
    # formfield_overrides = {
    #    models.TextField: {'provider': Select2TagWidget},
    # }
    list_select_related = ['provider']


@admin.register(models.Company)
class CompanyAdmin(BaseModelAdmin):
    PERMS = perms.CompanyPermissions
    list_display = ['name', 'created', 'updated']
    search_fields = ['name']
    sortable_by = ['name']
    #readonly_fields = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'inventory_mode') #, 'created', 'updated')
        }),
        # ('Filters', {
        #     'classes': ('expand',),
        #     'fields': ('providers', 'regions', 'resource_types'),
        # }),
    )

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()

        if not request.user.company:
            qs = qs.none()
        elif not request.user.is_superuser:
            qs = qs.filter(pk=request.user.company.pk)

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        return qs


@admin.register(models.Tag)
class TagAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.TagPermissions
    list_display = ('name', 'value', 'provider_name')
    search_fields = ['name']
    list_filter = ['provider', 'name']
    sortable_by = ['name', 'provider', 'value']
    # autocomplete_fields = ['provider']
    list_select_related = ['provider']


@admin.register(models.Resource)
class ResourceAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    PERMS = perms.ResourcePermissions
    list_display = ('name', 'resource_type_name', 'provider_name', 'company_name', 'active', 'locked')
    search_fields = ['resource_id', 'name']
    list_filter = [
        ('company', admin.RelatedOnlyFieldListFilter),
        #'provider', 
        ('active', admin.BooleanFieldListFilter), 
        #'locked'
    ]
    sortable_by = ['name', 'provider']
    autocomplete_fields = ['resource_type']  # , 'provider']
    list_select_related = ['company', 'resource_type', 'provider']
    #list_editable = ['active', 'locked']


@admin.register(models.ResourceEventChange)
class ResourceEventChangeAdmin(BaseModelAdminWithCompanyFieldMixin, ReadOnlyModelAdminMixIn, BaseModelAdmin):
    icon_name = 'access_time'
    date_hierarchy = 'created'
    list_display = ('object_id', '__str__', 'action', 'created')
    list_filter = ['action']
    list_filter = [
        ('created', PastDateRangeFilter),
        'action',
        #('action', admin.SimpleListFilter)
    ]
    list_select_related = ['content_type']
    readonly_fields = ['object_id', 'content_type', 'action', 'created']



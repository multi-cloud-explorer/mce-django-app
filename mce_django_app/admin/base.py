from django.contrib.admin import ModelAdmin

class BaseModelAdminWithCompanyFieldMixin:

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()

        if request.user.company:
            # print("!!! ok request.user.company")
            qs = qs.filter(company__pk=request.user.company.pk)
        elif not request.user.is_superuser:
            # print('!!! nok and not superuser')
            qs = qs.none()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        return qs


class BaseModelAdmin(ModelAdmin):

    PERMS = None

    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True
    view_on_site = False
    #actions_on_top = True
    #actions_on_bottom = True
    show_full_result_count = False # perfs
    #exclude = ['is_removed']

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #
    #     if not self.request.user.company:
    #         return self.queryset.model.objects.none()
    #
    #     return self.queryset.filter(company__pk=self.request.user.company.pk)
    #


    # def get_object(self, request, object_id, from_field=None):

    def has_module_permission(self, request):
        # print('!!! module : ', self.opts.app_label, self.model, request.user, request.method)
        return True

    def has_view_permission(self, request, obj=None):
        # print('!!! has_view_permission : ', request.user, obj, request.method)
        if request.user and request.user.is_superuser:
            return True

        if self.PERMS:
            return self.PERMS().has_permission(request, method="GET")

        return False

    def has_add_permission(self, request):
        # print('!!! has_add_permission : ', request.user, request.method)

        if self.PERMS:
            return self.PERMS().has_permission(request, method="POST")

        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        # print('!!! has_change_permission : ', self.model, request.user, obj, response, request.method)

        if self.PERMS:
            return self.PERMS().has_permission(request, method="PATCH")

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # print('!!! has_delete_permission : ', request.user, obj, request.method)

        if self.PERMS:
            return self.PERMS().has_permission(request, method="DELETE")

        return super().has_delete_permission(request, obj)


class ReadOnlyModelAdminMixIn:

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    # def has_module_permission(self, request):
    #     pass

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

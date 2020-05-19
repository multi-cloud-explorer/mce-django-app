from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu

"""
/mce/api/v1/doc/redoc/  drf_yasg.views.SchemaView       schema-redoc
/mce/api/v1/doc/swagger/        drf_yasg.views.SchemaView       schema-swagger-ui
"""


class CustomMenu(Menu):

    # class Media:
    #     css = {
    #         'all': ('test_app/menu.css',),
    #     }
    #     js = ('test_app/menu.js',)

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)

        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),

            # items.Bookmarks(),

            items.AppList(
                _('Applications'),
                #exclude=('django.contrib.*',)
                models=('mce_django_app.models.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.ModelList(
                title='Test app menu',
                models = [
                    'mce_django_app.models.common.Company',
                    'mce_django_app.models.common.Region',
                    'mce_django_app.models.common.ResourceType',
                    #'django.contrib.auth.*'
                ]
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        # print("!!! context : ", context, type(context))
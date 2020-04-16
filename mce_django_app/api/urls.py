from django.urls import path, include
from django.urls import re_path

from rest_framework.authtoken import views as authtoken_views
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Multi-Cloud-Explorer API",
      default_version='v1',
      description="Multi-Cloud-Explorer API Documentation",
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    #path('', include(router.urls)),
    path('common/', include('mce_django_app.api.common.urls')),
    path('azure/', include('mce_django_app.api.azure.urls')),
    path('api-token-auth/', authtoken_views.obtain_auth_token),
    re_path(r'^doc/swagger/(?P<format>\.json|\.yaml)/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.authtoken')),
]


from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'provider', views.ProviderViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'resource-type', views.ResourceTypeViewSet)
router.register(r'company', views.CompanyiewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'resource', views.ResourceViewSet)
router.register(r'resource-event-change', views.ResourceEventChangeViewSet)

urlpatterns = [
    path('', include((router.urls, 'common'))), #, namespace='instance_name'
]

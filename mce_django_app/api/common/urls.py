from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'resource-event-change', views.ResourceEventChangeViewSet)
router.register(r'generic-account', views.GenericAccountViewSet)
router.register(r'company', views.CompanyiewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'resource-type', views.ResourceTypeViewSet)
router.register(r'resource', views.ResourceViewSet)

urlpatterns = [
    path('', include((router.urls, 'common'))), #, namespace='instance_name'
]

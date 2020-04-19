from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'subscription', views.SubscriptionAzureViewSet)
router.register(r'resource-group', views.ResourceGroupAzureViewSet)
router.register(r'resource', views.ResourceAzureViewSet)

urlpatterns = [
    path('', include((router.urls, 'azure'))),
]

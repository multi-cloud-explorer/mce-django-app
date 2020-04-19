from rest_framework import viewsets
from rest_framework import permissions

from mce_django_app.models import azure as models

from . import serializers

class SubscriptionAzureViewSet(viewsets.ModelViewSet):

    queryset = models.SubscriptionAzure.objects.all()
    serializer_class = serializers.SubscriptionAzureSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResourceGroupAzureViewSet(viewsets.ModelViewSet):

    queryset = models.ResourceGroupAzure.objects.all().order_by('-created')
    serializer_class = serializers.ResourceGroupAzureSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResourceAzureViewSet(viewsets.ModelViewSet):

    #lookup_value_regex = '[/A-Za-z0-9.-]+'
    queryset = models.ResourceAzure.objects.all().order_by('-created')
    serializer_class = serializers.ResourceAzureSerializer
    permission_classes = [permissions.IsAuthenticated]

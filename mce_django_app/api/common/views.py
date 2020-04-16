from rest_framework import viewsets
from rest_framework import permissions

from mce_django_app.models import common as models

from . import serializers

# DjangoModelPermissions
# DjangoObjectPermissions

class ResourceEventChangeViewSet(viewsets.ModelViewSet):

    queryset = models.ResourceEventChange.objects.all().order_by('-updated', '-created')
    serializer_class = serializers.ResourceEventChangeSerializer
    permission_classes = [permissions.IsAuthenticated]


class GenericAccountViewSet(viewsets.ModelViewSet):

    queryset = models.GenericAccount.objects.all()
    serializer_class = serializers.GenericAccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyiewSet(viewsets.ModelViewSet):

    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResourceTypeViewSet(viewsets.ModelViewSet):

    queryset = models.ResourceType.objects.all()
    serializer_class = serializers.ResourceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResourceViewSet(viewsets.ModelViewSet):

    queryset = models.Resource.objects.all().order_by('-created')
    serializer_class = serializers.ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

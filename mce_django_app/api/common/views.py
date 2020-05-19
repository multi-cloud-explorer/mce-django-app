#from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets
#from rest_framework import authentication, generics, serializers, status
#from rest_framework_guardian.filters import ObjectPermissionsFilter
#from djoser.permissions import CurrentUserOrAdmin, CurrentUserOrAdminOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from mce_django_app.models import common as models

from mce_django_app.api import perms

from . import serializers

# class CustomObjectPermissions(permissions.DjangoObjectPermissions):
#     """
#     Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
#     """
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
#         'HEAD': ['%(app_label)s.view_%(model_name)s'],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

from rest_framework import status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError

class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            return Response(status=status.HTTP_423_LOCKED, data={'detail':str(e)})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail':str(e)})

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class WithCompanyFieldMixin:

    permission_classes = [perms.TagPermissions]

    def get_queryset(self):
        if not self.request.user.is_active:
            return self.queryset.model.objects.none()

        if self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(company__pk=self.request.user.company.pk)


class ProviderViewSet(viewsets.ModelViewSet):

    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    #permission_classes = [perms.MCEPermissions]


class RegionViewSet(viewsets.ModelViewSet):

    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ResourceTypeViewSet(viewsets.ModelViewSet):

    queryset = models.ResourceType.objects.all()
    serializer_class = serializers.ResourceTypeSerializer
    #permission_classes = [permissions.IsAuthenticated]


class CompanyiewSet(DestroyModelMixin, viewsets.ModelViewSet):

    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [perms.CompanyPermissions]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        if not self.request.user.company:
            return self.queryset.model.objects.none()

        return self.queryset.filter(pk=self.request.user.company.pk)


class TagViewSet(WithCompanyFieldMixin, viewsets.ModelViewSet):

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    # permission_classes = [perms.TagPermissions]

    # def get_queryset(self):
    #     if not self.request.user.is_active:
    #         return self.queryset.model.objects.none()
    #
    #     if self.request.user.is_superuser:
    #         return self.queryset
    #
    #     return self.queryset.filter(company__pk=self.request.user.company.pk)


class ResourceViewSet(WithCompanyFieldMixin, DestroyModelMixin, viewsets.ModelViewSet):

    # TODO: read only !

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    queryset = models.Resource.objects.all().order_by('-created')
    serializer_class = serializers.ResourceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [ObjectPermissionsFilter]

    # def destroy(self, *args, **kwargs):
    #     #serializer = self.get_serializer(self.get_object())
    #     super().destroy(*args, **kwargs)
    #     return Response(status=status.HTTP_200_OK)
    #     #return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        print('!!! self.action : ', self.action)
        # create / patch=partial_update
        if self.action in ['list', 'retrieve']:
            return serializers.ResourceSerializer
        else:
            return serializers.ResourceSerializerDetail

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        if not self.request.user.company:
            return self.queryset.model.objects.none()

        return self.queryset.filter(company__pk=self.request.user.company.pk)

class ResourceEventChangeViewSet(viewsets.ModelViewSet):

    queryset = models.ResourceEventChange.objects.all().order_by('-updated', '-created')
    serializer_class = serializers.ResourceEventChangeSerializer
    # permission_classes = [permissions.IsAuthenticated]



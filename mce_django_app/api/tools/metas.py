from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mce_django_app.api.common import serializers as common
from mce_django_app.api.metadata import APIMetadata

# TODO: perms
class Metas(APIView):

    def get(self, request, format=None):
        metadata_generator = APIMetadata()
        metas = {}
        metas["provider"] = metadata_generator.get_serializer_info(common.ProviderSerializer())
        metas["region"] = metadata_generator.get_serializer_info(common.RegionSerializer())
        metas["resourcetype"] = metadata_generator.get_serializer_info(common.ResourceTypeSerializer())
        metas["company"] = metadata_generator.get_serializer_info(common.CompanySerializer())
        return Response(metas)
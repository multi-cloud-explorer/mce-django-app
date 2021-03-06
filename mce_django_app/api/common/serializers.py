from rest_framework import serializers

from mce_django_app.models import common as models

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provider
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = '__all__'


class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceType
        fields = '__all__'


class SyncSettingsSerializer(serializers.ModelSerializer):

    include_providers = serializers.HyperlinkedIdentityField(
        view_name="common:provider-detail",
        many=True,
        read_only=True
    )
    exclude_providers = serializers.HyperlinkedIdentityField(
        view_name="common:provider-detail",
        many=True,
        read_only=True
    )

    include_regions = RegionSerializer(many=True, read_only=True)
    exclude_regions = RegionSerializer(many=True, read_only=True)

    include_resource_types = RegionSerializer(many=True, read_only=True)
    exclude_resource_types = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = models.SyncSettings
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    # TODO: settings

    class Meta:
        model = models.Company
        fields = '__all__'
        # read_only_fields = [
        #     'id',
        #     'slug',
        #     'created',
        #     'updated',
        # ]


class TagSerializer(serializers.ModelSerializer):

    provider = serializers.HyperlinkedIdentityField(
        view_name="common:provider-detail",
        read_only=True
    )

    company = serializers.HyperlinkedIdentityField(
        view_name="common:company-detail",
        read_only=True
    )

    class Meta:
        model = models.Tag
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):

    provider = serializers.HyperlinkedIdentityField(
        view_name="common:provider-detail",
        # read_only=True
    )

    resource_type = serializers.HyperlinkedIdentityField(
        view_name="common:resourcetype-detail",
        # read_only=True
    )

    company = serializers.HyperlinkedIdentityField(
        view_name="common:company-detail",
        # read_only=True
    )

    tags = serializers.HyperlinkedIdentityField(
        view_name="common:tag-detail",
        many=True,
        read_only=True # TODO: ?
    )

    metas = serializers.JSONField(read_only=True)

    class Meta:
        model = models.Resource
        fields = '__all__'

class ResourceSerializerDetail(serializers.ModelSerializer):

    metas = serializers.DictField(child=serializers.CharField(), allow_empty=False, required=True)

    #tags = TagSerializer(many=True)

    class Meta:
        model = models.Resource
        fields = [
            'id',
            'name',
            'resource_id',
            'company',
            'provider',
            'resource_type',
            'metas'
        ]

class ResourceEventChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceEventChange
        fields = '__all__'


from rest_framework import serializers

from mce_django_app.models import common as models

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        fields = '__all__'


class ResourceEventChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceEventChange
        fields = '__all__'


# class GenericAccountSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.GenericAccount
#         fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceType
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):

    #resource_type = serializers.SerializerMethodField()
    resource_type = ResourceTypeSerializer(read_only=True)

    company = CompanySerializer(read_only=True)

    #tags = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    #def get_resource_type(self, obj):
    #    return obj.resource_type.name

    #def get_tags(self, obj):
    #    return [{tag.name: tag.value} for tag in obj.tags.all()]

    class Meta:
        model = models.Resource
        fields = '__all__'



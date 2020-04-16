from rest_framework import serializers

from mce_django_app.models import common as models

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        exclude = ['is_removed']

class ResourceEventChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceEventChange
        exclude = ['is_removed']

class GenericAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GenericAccount
        exclude = ['is_removed']

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        exclude = ['is_removed']

class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceType
        exclude = ['is_removed']

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
        exclude = ['is_removed']


from rest_framework import serializers

from mce_django_app.api.common.serializers import ResourceSerializer, GenericAccountSerializer

from mce_django_app.models import azure as models

class SubscriptionAzureSerializer(serializers.ModelSerializer):

    account = GenericAccountSerializer(read_only=True)

    class Meta:
        model = models.SubscriptionAzure
        fields = '__all__'


class ResourceGroupAzureSerializer(ResourceSerializer):

    subscription = SubscriptionAzureSerializer(read_only=True)

    class Meta:
        model = models.ResourceGroupAzure
        fields = '__all__'


class ResourceAzureSerializer(ResourceSerializer):

    subscription = SubscriptionAzureSerializer(read_only=True)

    resource_group = ResourceGroupAzureSerializer(read_only=True)

    # sku = utils.JSONField

    class Meta:
        model = models.ResourceAzure
        fields = '__all__'



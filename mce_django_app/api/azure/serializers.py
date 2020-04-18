from rest_framework import serializers

from mce_django_app.api.common.serializers import ResourceSerializer, GenericAccountSerializer

from mce_django_app.models import azure as models

class SubscriptionSerializer(serializers.ModelSerializer):

    account = GenericAccountSerializer(read_only=True)

    class Meta:
        model = models.Subscription
        fields = '__all__'


class ResourceGroupAzureSerializer(ResourceSerializer):

    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = models.ResourceGroupAzure
        fields = '__all__'


class ResourceAzureSerializer(ResourceSerializer):

    subscription = SubscriptionSerializer(read_only=True)

    resource_group = ResourceGroupAzureSerializer(read_only=True)

    # sku = utils.JSONField

    class Meta:
        model = models.ResourceAzure
        fields = '__all__'



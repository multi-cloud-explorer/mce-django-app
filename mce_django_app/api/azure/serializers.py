from rest_framework import serializers

from mce_django_app.api.common.serializers import ResourceSerializer, GenericAccountSerializer

from mce_django_app.models import azure as models

class SubscriptionSerializer(serializers.ModelSerializer):

    account = GenericAccountSerializer(read_only=True)

    class Meta:
        model = models.Subscription
        exclude = ['is_removed']


class ResourceGroupAzureSerializer(ResourceSerializer):

    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = models.ResourceGroupAzure
        exclude = ['is_removed']


class ResourceAzureSerializer(ResourceSerializer):

    subscription = SubscriptionSerializer(read_only=True)

    resource_group = ResourceGroupAzureSerializer(read_only=True)

    # sku = utils.JSONField

    class Meta:
        model = models.ResourceAzure
        exclude = ['is_removed']



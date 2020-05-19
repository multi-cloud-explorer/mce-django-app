from rest_framework import viewsets
from rest_framework import permissions

from mce_django_app.models import azure as models

from . import serializers

class SubscriptionAzureViewSet(viewsets.ModelViewSet):

    queryset = models.SubscriptionAzure.objects.all()
    serializer_class = serializers.SubscriptionAzureSerializer
    permission_classes = [permissions.IsAuthenticated]

# class ResourceGroupAzureViewSet(viewsets.ModelViewSet):
#
#     queryset = models.ResourceGroupAzure.objects.all().order_by('-created')
#     serializer_class = serializers.ResourceGroupAzureSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ResourceAzureViewSet(viewsets.ModelViewSet):

    #lookup_value_regex = '[/A-Za-z0-9.-]+'
    queryset = models.ResourceAzure.objects.all().order_by('-created')
    serializer_class = serializers.ResourceAzureSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Pour créer des Tag en même temps :
    # def create(self, validated_data):
    #     tags_data = validated_data.pop('tags')
    #     doc = self.queryset.model.objects.create(**validated_data)
    #     for tag in tags_data:
    #         models.Tag.objects.create(company=doc.company, provider=doc.provider, **tag)
    #     return doc
    #
    # def update(self, instance, validated_data):
    #     albums_data = validated_data.pop('album_musician')
    #     albums = (instance.album_musician).all()
    #     albums = list(albums)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.instrument = validated_data.get('instrument', instance.instrument)
    #     instance.save()
    #
    #     for album_data in albums_data:
    #         album = albums.pop(0)
    #         album.name = album_data.get('name', album.name)
    #         album.release_date = album_data.get('release_date', album.release_date)
    #         album.num_stars = album_data.get('num_stars', album.num_stars)
    #         album.save()
    #     return instance


"""
TODO: vue hors model pour recevoir request create REST:
    - Que tableau même si un seul élément

    - Company déduit du user.company
    - Déduit par le champs id:
        - subscription
        - subscription_id
        - resource group
    - Region du champs location
    {
        "name": "MY_VM",
        "id": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/MY_RG_GROUP/providers/Microsoft.Compute/virtualMachines/MY_VM",
        "type": "Microsoft.Compute/virtualMachines",
        "location": "westeurope",
        "tags": {
            "hidden-DevTestLabs-LogicalResourceUId": "00000000-0000-0000-0000-000000000000"
        },
        "properties": {}
    }


    resource_id="x1",
    name="myname",
    company=mce_app_company.pk,
    resource_type=mce_app_resource_type.pk,
    provider=mce_app_resource_type.provider.pk,
    metas={"key1": "value1"},

"""
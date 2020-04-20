from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app.models.common import (
    Resource,
    BaseSubscription,
    ResourceEventChange,
)

# TODO: Azure Account avec tenant optionnel


class SubscriptionAzure(BaseSubscription):
    """Cloud Subscription Model"""

    tenant = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    is_china = models.BooleanField(default=False)

    def get_auth(self):
        """Auth format for `mce_azure.utils.get_access_token`"""

        data = dict(
            subscription_id=self.subscription_id,
            tenant=self.tenant,
            user=None,
            password=None,
            is_china=self.is_china,
        )
        if self.account:
            data["user"] = self.account.username
            data["password"] = self.account.password
        return data


class ResourceGroupAzure(Resource):

    location = models.CharField(max_length=255)

    subscription = models.ForeignKey(SubscriptionAzure, on_delete=models.PROTECT)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['subscription'] = self.subscription.subscription_id
        return data


class ResourceAzure(Resource):

    # Que 46 sur 421 ont un kind !!!
    kind = models.CharField(max_length=255, null=True, blank=True)

    location = models.CharField(max_length=255)

    subscription = models.ForeignKey(SubscriptionAzure, on_delete=models.PROTECT)

    resource_group = models.ForeignKey(ResourceGroupAzure, on_delete=models.PROTECT)

    # TODO: clean(): control si même provider que souscription

    sku = utils.JSONField(default={}, null=True, blank=True)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['subscription'] = self.subscription.subscription_id
        data['resource_group'] = self.resource_group.name
        if self.sku:
            data['sku'] = dict(self.sku)
        return data

"""
TODO: class ResourceAzureVM(ResourceAzure):

properties: dict = {}
plan: dict = {}
managedBy: str = None

dns_name
ip_address
os_type
os_name
state (si vm : started|stopped)
sync_state: new|???
geo localisation ?
"""



def _create_event_change(sender, instance=None, created=None, **kwargs):
    if created:
        ResourceEventChange.objects.create(
            action=constants.EventChangeType.CREATE,
            content_object=instance,
            new_object=instance.to_dict(exclude=['created', 'updated']),
        )

@receiver(post_save, sender=ResourceAzure)
def resource_create_event_change(sender, instance=None, created=None, **kwargs):
    _create_event_change(sender, instance=instance, created=created, **kwargs)

@receiver(post_save, sender=ResourceGroupAzure)
def resource_group_create_event_change(sender, instance=None, created=None, **kwargs):
    _create_event_change(sender, instance=instance, created=created, **kwargs)

# post_delete: faux delete si soft delete !!!


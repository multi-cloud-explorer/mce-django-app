from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.conf import settings

from django_cryptography.fields import encrypt
from jsonfield import JSONField

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app import signals

from mce_django_app.models.common import (
    Resource,
    BaseSubscription,
)

# TODO: Azure Account avec tenant optionnel


class SubscriptionAzure(BaseSubscription):
    """Cloud Subscription Model"""

    username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"), null=True, blank=True)

    password = encrypt(
        models.CharField(max_length=255, verbose_name=_("Password or Secret Key"), null=True, blank=True)
    )

    tenant = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    is_china = models.BooleanField(default=False)

    def get_auth(self):
        """Auth format for `mce_azure.utils.get_access_token`"""

        # TODO: control
        data = dict(
            subscription_id=self.subscription_id,
            tenant=self.tenant,
            user=self.username,
            password=self.password,
            is_china=self.is_china,
        )
        #if self.account:
        #    data["user"] = self.account.username
        #    data["password"] = self.account.password
        return data

# # TODO: supprimer. Devient un ForeingKey(self) dans Resource
# class ResourceGroupAzure(Resource):
#
#     location = models.CharField(max_length=255)
#
#     subscription = models.ForeignKey(SubscriptionAzure, on_delete=models.PROTECT)
#
#     def to_dict(self, fields=None, exclude=None):
#         data = super().to_dict(fields=fields, exclude=exclude)
#         data['subscription'] = self.subscription.subscription_id
#         return data


class ResourceAzure(Resource):

    # Que 46 sur 421 ont un kind !!!
    kind = models.CharField(max_length=255, null=True, blank=True)

    location = models.CharField(max_length=255)

    subscription = models.ForeignKey(SubscriptionAzure, on_delete=models.PROTECT)

    resource_group = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    # TODO: clean(): control si même provider que souscription
    @property
    def tenant(self):
        return self.subscription.tenant

    @property
    def subscription_name(self):
        return self.subscription.name

    @property
    def resource_group_name(self):
        return self.resource_group.name

    def clean_fields(self, exclude=None):
        errors = {}
        try:
            super().clean_fields(exclude=exclude)
        except ValidationError as err:
            errors = err.error_dict
        if not self.resource_group and self.resource_type and self.resource_type.name.lower() != "microsoft.resources/resourcegroups":
            errors['resource_group'] = ValidationError(_("This field cannot be null."), code="required")

        if errors:
            raise ValidationError(errors)

    sku = JSONField(default={}, null=True, blank=True)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['subscription'] = self.subscription.subscription_id
        if self.resource_group:
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

if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceAzure)
    def resource_azure_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)


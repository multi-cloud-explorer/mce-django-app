from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.conf import settings

from django_cryptography.fields import encrypt
from jsonfield import JSONField
from django_extensions.db.fields import AutoSlugField

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app import signals

from mce_django_app.models.common import (
    BaseModel, Resource, Region, Provider, Company)

__all__ = [
    'SubscriptionAzure',
    'ResourceAzure'
]


class SubscriptionAzure(BaseModel):
    """Cloud Subscription Model"""

    subscription_id = models.CharField(
        unique=True,
        max_length=1024
    )

    slug = AutoSlugField(
        max_length=1024,
        populate_from=['subscription_id'],
        overwrite=True,
        unique=True
    )

    name = models.CharField(max_length=255)

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss"
    )

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, default=constants.Provider.AZURE)

    active = models.BooleanField(default=True)

    username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"), null=True, blank=True)

    password = encrypt(
        models.CharField(max_length=255, verbose_name=_("Password or Secret Key"), null=True, blank=True)
    )

    # TODO: Model
    tenant = models.CharField(max_length=255)

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
        return data

    @property
    def company_name(self):
        return self.company.name

    @property
    def provider_name(self):
        return self.provider.name

    def __str__(self):
        return f"{self.provider.name} - {self.name}"

    class Meta:
        verbose_name = _("Azure Subscription")
        verbose_name_plural = _("Azure Subscriptions")

class ResourceAzure(Resource):

    subscription = models.ForeignKey(SubscriptionAzure, on_delete=models.CASCADE)

    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    # Que 46 sur 421 ont un kind !!!
    kind = models.CharField(max_length=255, null=True, blank=True)

    # "sku": {
    #     "name": "Standard_LRS",
    #     "tier": "Standard"
    # }
    sku = JSONField(default={}, null=True, blank=True)

    # TODO: utiliser un champs CharField pour faire plus simple ?
    resource_group = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        #related_name="resources",
        null=True, blank=True
    )

    # "plan": {
    #     "name": "ContainerInsights(log)",
    #     "publisher": "Microsoft",
    #     "promotionCode": "",
    #     "product": "OMSGallery/ContainerInsights"
    # }
    plan = JSONField(default={}, null=True, blank=True)

    # TODO: Attention, basé sur resource_id
    # TODO: utiliser un champs CharField pour faire plus simple ?
    managed_by = models.CharField(max_length=1024, null=True, blank=True)
    # managed_by = models.ForeignKey(
    #     'self',
    #     on_delete=models.PROTECT,
    #     # related_name="resources",
    #     null=True, blank=True
    # )

    @property
    def tenant(self):
        return self.subscription.tenant

    @property
    def subscription_name(self):
        return self.subscription.name

    @property
    def resource_group_name(self):
        if self.resource_group:
            return self.resource_group.name

    @property
    def region_name(self):
        return self.region.name

    def clean_fields(self, exclude=None):
        errors = {}

        try:
            super().clean_fields(exclude=exclude)
        except ValidationError as err:
            errors = err.error_dict

        if getattr(self, 'subscription', None):
            if self.subscription.provider.pk != self.provider.pk:
                msg = f"Provider [{self.provider}] is not same of Subscription Provider [{self.subscription.provider.name}]."
                errors["provider"] = ValidationError(_(msg))

        if getattr(self, 'resource_group', None) and getattr(self, 'resource_type', None):
            if not self.resource_group and self.resource_type and self.resource_type.name.lower() != "microsoft.resources/resourcegroups":
                errors['resource_group'] = ValidationError(_("This field cannot be null."), code="required")

        if errors:
            raise ValidationError(errors)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)

        data['subscription'] = self.subscription.subscription_id
        data['region'] = self.region.name

        if self.resource_group:
            data['resource_group'] = self.resource_group.name

        if self.managed_by:
            data['managed_by'] = self.managed_by.name

        return data

    class Meta:
        verbose_name = _("Azure Resource")
        verbose_name_plural = _("Azure Resources")


"""
TODO: class ResourceAzureVM(ResourceAzure): ?
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


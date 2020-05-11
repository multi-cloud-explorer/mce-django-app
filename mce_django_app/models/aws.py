from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django_cryptography.fields import encrypt
from django_extensions.db.fields import AutoSlugField

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app import signals

from mce_django_app.models.common import BaseModel, Resource, Provider, Region, Company

__all__ = [
    'SubscriptionAWS',
    'ResourceAWS'
]


class SubscriptionAWS(BaseModel):
    """AWS Subscription Model"""

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

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    active = models.BooleanField(default=True)

    # TODO: choice de la liste des régions
    default_region = models.CharField(max_length=255, null=True, blank=True)

    username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"), null=True, blank=True)

    password = encrypt(
        models.CharField(max_length=255, verbose_name=_("Password or Secret Key"), null=True, blank=True)
    )

    assume_role = models.CharField(max_length=255, verbose_name=_("Assume Role"), null=True, blank=True)

    #profile_name = models.CharField(max_length=255, verbose_name=_("Profile Name"), null=True, blank=True)

    def get_auth(self):
        """Auth format for `mce_lib_aws.???`"""

        data = dict(
            subscription_id=self.subscription_id,
            user=self.username,
            password=self.password,
            assume_role=self.assume_role,
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
        verbose_name = _("AWS Subscription")
        verbose_name_plural = _("AWS Subscriptions")


class ResourceAWS(Resource):

    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    subscription = models.ForeignKey(SubscriptionAWS, on_delete=models.PROTECT)

    @property
    def subscription_name(self):
        return self.subscription.name

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

        return data

    class Meta:
        verbose_name = _("AWS Resource")
        verbose_name_plural = _("AWS Resources")


if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceAWS)
    def resource_aws_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)

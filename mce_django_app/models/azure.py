from django.db import models
from django.utils.translation import ugettext_lazy as _

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app.models.common import BaseModel, Resource, GenericAccount

# TODO: Azure Account avec tenant optionnel


class Subscription(BaseModel):
    """Cloud Subscription Model"""

    id = models.UUIDField(primary_key=True, max_length=255)

    name = models.CharField(max_length=255)

    tenant = models.UUIDField(max_length=255)

    location = models.CharField(max_length=255)

    is_china = models.BooleanField(default=False)

    # TODO: limit_choices_to={''}
    provider = models.CharField(
        max_length=255,
        default=constants.Provider.AZURE,
        choices=constants.Provider.choices,
        editable=False,
    )

    account = models.ForeignKey(
        GenericAccount,
        related_name="subscriptions_azure",
        on_delete=models.PROTECT,
        null=True,
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_auth(self):
        """Auth format for `mce_azure.utils.get_access_token`"""

        data = dict(
            subscription_id=str(self.pk),
            tenant=str(self.tenant),
            user=None,
            password=None,
            is_china=self.is_china,
        )
        if self.account:
            data["user"] = self.account.username
            data["password"] = self.account.password
        return data

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['id'] = str(self.pk)
        return data


class ResourceGroupAzure(Resource):

    location = models.CharField(max_length=255)

    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['subscription'] = str(self.subscription.pk)
        return data


class ResourceAzure(Resource):

    # Que 46 sur 421 ont un kind !!!
    kind = models.CharField(max_length=255, null=True, blank=True)

    location = models.CharField(max_length=255)

    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)

    resource_group = models.ForeignKey(ResourceGroupAzure, on_delete=models.PROTECT)

    # TODO: clean(): control si même provider que souscription

    sku = utils.JSONField(default={}, null=True, blank=True)

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data['subscription'] = str(self.subscription.pk)
        data['resource_group'] = self.resource_group.name
        if self.sku:
            data['sku'] = dict(self.sku)
        return data

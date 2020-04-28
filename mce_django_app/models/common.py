from itertools import chain

from furl import furl

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField
from django_cryptography.fields import encrypt

from mce_django_app import utils
from mce_django_app import constants

__all__ = [
    'BaseModel',
    'BaseSubscription',
    'Provider',
    'Company',
    'Tag',
    'ResourceType',
    'Resource',
    'ResourceEventChange',
]

# TODO: order_by default and others Metas
# TODO: permissions ? owner/owner_group ?

class BaseModel(models.Model):
    """Base for all MCE models"""

    created = models.DateTimeField(auto_now_add=True, editable=False)

    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        """Update updated field and Call :meth:`full_clean` before saving."""

        if not self._state.adding:
            self.updated = timezone.now()

        self.full_clean()

        super().save(*args, **kwargs)

    def to_dict(self, fields=None, exclude=None):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            # if not getattr(f, 'editable', False):
            #    continue
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        abstract = True

class Provider(BaseModel):

    name = models.CharField(max_length=255, unique=True, choices=constants.Provider.choices)

    slug = AutoSlugField(
                            max_length=300,
                            populate_from=['name'],
                            overwrite=True,
                            unique=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Company(BaseModel):

    # TODO: is_default !!!
    # TODO: unique ?
    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(populate_from=['name'], overwrite=True, unique=True)

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")


class ResourceEventChange(BaseModel):

    action = models.CharField(max_length=10, choices=constants.EventChangeType.choices)

    changes = utils.JSONField(default=[], null=True, blank=True)

    old_object = utils.JSONField(default={}, null=True, blank=True)

    new_object = utils.JSONField(default={}, null=True, blank=True)

    diff = models.TextField(null=True, blank=True)

    # TODO: on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    #object_id = models.CharField(max_length=1024, verbose_name=_("Id"))
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type', 'object_id', for_concrete_model=True
    )

    # TODO: state: new|sended|consumed
    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data["content_type"] = {
            "app_label": self.content_type.app_label,
            "model": self.content_type.model,
            "name": self.content_type.name,
            "id": self.object_id
        }
        return data

    def to_json(self, fields=None, exclude=None):
        from django.core import serializers
        data = self.to_dict(fields=fields, exclude=exclude)
        #json.dumps(data, cls=DjangoJSONEncoder, indent=4)

    def __str__(self):
        return f"{self.content_type.app_label}.{self.content_type.model}: {self.object_id}"


# class GenericAccount(BaseModel):
#     """Store Login/Password"""
#
#     # TODO: settings pour auth et forms spécifique
#
#     name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
#
#     description = models.CharField(
#         max_length=255, null=True, blank=True, verbose_name=_("Description")
#     )
#
#     url = models.CharField(max_length=2048, null=True, blank=True)
#
#     username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"), null=True, blank=True)
#
#     password = encrypt(
#         models.CharField(max_length=255, verbose_name=_("Password or Secret Key"), null=True, blank=True)
#     )
#
#     # TODO: null=True pour compte hors Company ?
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#
#     settings = encrypt(utils.JSONField(default={}, null=True, blank=True))
#
#     @classmethod
#     def parse_url(cls, url):
#         url = furl(url)
#         base_url = url.origin + str(url.path)
#         data = dict(url.args) or {}
#         return (base_url, data)
#
#     def save(self, **kwargs):
#         if self.url and "?" in self.url:
#             url, settings = GenericAccount.parse_url(self.url)
#             if settings:
#                 self.settings.update(settings)
#                 self.url = url
#         super().save(**kwargs)
#
#     def __str__(self):
#         return f"{self.name} ({self.description})"


class Tag(BaseModel):
    """Cloud Tags"""

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    value = models.CharField(max_length=1024)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, null=True, blank=True)

    @property
    def provider_name(self):
        return self.provider.name

    def to_dict(self, fields=None, exclude=[]):
        data = super().to_dict(fields=fields, exclude=exclude)
        if self.provider:
            data["provider"] = self.provider.name
        return data

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "name", "value"], name='provider_name_value_uniq'
            ),
            models.UniqueConstraint(
                fields=['name', 'value'],
                name='name_value_without_provider_uniq',
                condition=models.Q(provider__isnull=True),
            ),
        ]

    def __str__(self):
        return self.name


# TODO: Faire BaseRegion ou BaseLocation pour tous ?

class BaseSubscription(BaseModel):
    """Base for Subscription Model"""

    subscription_id = models.CharField(unique=True, max_length=1024)

    # TODDDDO: slug = AutoSlugField(
    #                         max_length=1024,
    #                         populate_from=['subscription_id'],
    #                         overwrite=True,
    #                         unique=True)

    name = models.CharField(max_length=255)

    company = models.ForeignKey(
        Company, on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss"
    )

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    #account = models.ForeignKey(
    #    GenericAccount,
    #    on_delete=models.SET_NULL,
    #    null=True,
    #    related_name="%(app_label)s_%(class)s_related",
    #    related_query_name="%(app_label)s_%(class)ss",
    #)

    active = models.BooleanField(default=True)

    @property
    def company_name(self):
        return self.company.name

    @property
    def provider_name(self):
        return self.provider.name

    def get_auth(self):
        raise NotImplementedError()

    def __str__(self):
        return f"{self.provider.name} - {self.name}"
    
    class Meta:
        abstract = True


class ResourceType(BaseModel):

    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(
                            max_length=1024, 
                            populate_from=['name'], 
                            overwrite=True, 
                            unique=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    exclude_sync = models.BooleanField(default=False)

    @property
    def provider_name(self):
        return self.provider.name

    def __str__(self):
        return f"{self.provider.name} - {self.name}"


class Resource(BaseModel):
    """Generic Resource"""

    resource_id = models.CharField(unique=True, max_length=1024)

    slug = AutoSlugField(max_length=1024, populate_from=['resource_id'], 
                        slugify_function=utils.slugify_resource_id_function, 
                        overwrite=True, unique=True)

    name = models.CharField(max_length=255)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    # TODO: limit choices same provider
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    # TODO: limit choices same provider
    tags = models.ManyToManyField(Tag)

    metas = encrypt(utils.JSONField(default={}, null=True, blank=True))

    changes = GenericRelation(ResourceEventChange, related_query_name='resource')

    locked = models.BooleanField(default=False)

    active = models.BooleanField(default=True)

    @property
    def company_name(self):
        return self.company.name

    @property
    def resource_type_name(self):
        return self.resource_type.name

    @property
    def provider_name(self):
        return self.provider.name

    def __str__(self):
        return f"{self.provider.name} - {self.resource_type_name} - {self.name}"

    def to_dict(self, fields=None, exclude=[]):
        exclude = exclude or []
        exclude.append("changes")
        exclude.append("resource_ptr")

        data = super().to_dict(fields=fields, exclude=exclude)
        data['resource_type'] = self.resource_type.name
        data['company'] = self.company.name
        data['provider'] = str(self.provider.name)

        if self.metas:
            data['metas'] = dict(self.metas)

        data["tags"] = [tag.to_dict(fields=["name", "value", "provider"]) for tag in self.tags.all()]

        return data


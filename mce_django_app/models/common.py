from itertools import chain

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
    'Company',
    'GenericAccount',
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


class Company(BaseModel):

    name = models.CharField(max_length=255)

    slug = AutoSlugField(populate_from=['name'], overwrite=True, unique=True, blank=False)

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")


class ResourceEventChange(BaseModel):

    action = models.CharField(max_length=10, choices=constants.EventChangeType.choices)

    changes = utils.JSONField(default=[], null=True, blank=True)

    old_object = utils.JSONField(default={}, null=True, blank=True)

    new_object = utils.JSONField(default={}, null=True, blank=True)

    diff = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    #object_id = models.CharField(max_length=1024, verbose_name=_("Id"))
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type', 'object_id', for_concrete_model=False
    )

    # TODO: state: new|sended|consumed

    def __str__(self):
        return f"{self.content_type.app_label}.{self.content_type.model}: {self.object_id}"


class GenericAccount(BaseModel):
    """Store Login/Password"""

    # TODO: settings pour auth et forms spécifique

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Description")
    )

    url = models.CharField(max_length=2048, null=True, blank=True)

    username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"), null=True, blank=True)

    password = encrypt(
        models.CharField(max_length=255, verbose_name=_("Password or Secret Key"), null=True, blank=True)
    )

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    settings = utils.JSONField(default={}, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.description})"


class Tag(BaseModel):
    """Cloud Tags"""

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    value = models.CharField(max_length=1024)

    provider = models.CharField(
        max_length=255, choices=constants.Provider.choices, null=True, blank=True
    )

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


class BaseSubscription(BaseModel):
    """Base for Subscription Model"""

    subscription_id = models.CharField(unique=True, max_length=1024)

    name = models.CharField(max_length=255)

    company = models.ForeignKey(
        Company, on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss"
    )

    account = models.ForeignKey(
        GenericAccount,
        on_delete=models.PROTECT,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    active = models.BooleanField(default=True)

    def get_auth(self):
        raise NotImplementedError()

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True


class ResourceType(BaseModel):

    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(
                            max_length=1024, 
                            populate_from=['name'], 
                            overwrite=True, 
                            unique=True, 
                            blank=False)

    description = models.CharField(max_length=255, null=True, blank=True)

    provider = models.CharField(max_length=255, choices=constants.Provider.choices)

    # TODO: active ou exclude

    def __str__(self):
        return f"{self.provider} - {self.name}"


class Resource(BaseModel):
    """Generic Resource"""

    # TODO: vmware ? construire ID sur même model que Azure
    resource_id = models.CharField(unique=True, max_length=1024)

    slug = AutoSlugField(max_length=1024, populate_from=['resource_id'], 
                        slugify_function=utils.slugify_resource_id_function, 
                        overwrite=True, unique=True, blank=False)

    name = models.CharField(max_length=255)

    provider = models.CharField(max_length=255, choices=constants.Provider.choices)

    # TODO: limit choices same provider
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)

    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    # TODO: limit choices same provider
    tags = models.ManyToManyField(Tag)

    metas = utils.JSONField(default={}, null=True, blank=True)

    changes = GenericRelation(ResourceEventChange, related_query_name='resource')

    locked = models.BooleanField(default=False)

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.resource_id})"

    def to_dict(self, fields=None, exclude=[]):
        exclude = exclude or []
        exclude.append("changes")
        exclude.append("resource_ptr")

        data = super().to_dict(fields=fields, exclude=exclude)
        data['resource_type'] = self.resource_type.name
        data['company'] = self.company.name

        if self.metas:
            data['metas'] = dict(self.metas)

        data["tags"] = [tag.to_dict(exclude=exclude) for tag in self.tags.all()]

        return data


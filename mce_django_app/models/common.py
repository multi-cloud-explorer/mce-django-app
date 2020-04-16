from itertools import chain

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField
from model_utils.models import SoftDeletableModel
from model_utils.managers import SoftDeletableManager, SoftDeletableQuerySet
from django_cryptography.fields import encrypt

from mce_django_app import utils
from mce_django_app import constants

__all__ = [
    'BaseModel',
    'GenericAccount',
    'Tag',
    'ResourceType',
    'Resource',
    'ResourceEventChange',
]

# TODO: order_by default and others Metas


class CustomSoftDeletableQuerySet(SoftDeletableQuerySet):
    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        return self.update(is_removed=True)


class CustomSoftDeletableManager(SoftDeletableManager):

    _queryset_class = CustomSoftDeletableQuerySet


# TODO: permissions ? owner/owner_group ?
class BaseModel(SoftDeletableModel):
    """Base for all MCE models
    
    Model.objects return only is_removed=False
    
    Use Model.all_objects for all datas
    """

    objects = CustomSoftDeletableManager()

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

class ResourceEventChange(BaseModel):

    action = models.CharField(max_length=10, choices=constants.EventChangeType.choices)

    changes = utils.JSONField(default=[], null=True, blank=True)

    old_object = utils.JSONField(default={}, null=True, blank=True)

    new_object = utils.JSONField(default={}, null=True, blank=True)

    diff = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.CharField(max_length=1024)

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

    username = models.CharField(max_length=255, verbose_name=_("Username or Client ID"))

    password = encrypt(
        models.CharField(max_length=255, verbose_name=_("Password or Secret Key"))
    )

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


class ResourceType(BaseModel):

    name = models.CharField(max_length=255, unique=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    provider = models.CharField(max_length=255, choices=constants.Provider.choices)

    def __str__(self):
        return f"{self.provider} - {self.name}"


class Resource(BaseModel):
    """"""

    """
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

    """
    def slugify_function(self, content):
        v = utils.slugify_resource_id_function(content)
        print('!!!!!!!!! slugify_function ', content, v)
        return v
    """

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

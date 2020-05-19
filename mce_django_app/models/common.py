from furl import furl
import jsonpatch

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#from guardian.shortcuts import assign_perm
from django_extensions.db.fields import AutoSlugField
from django_cryptography.fields import encrypt
from jsonfield import JSONField
from taggit.managers import TaggableManager

from mce_django_app import utils
from mce_django_app import constants

__all__ = [
    'BaseModel',
    'Provider',
    'Region',
    'SyncSettings',
    'Company',
    'Tag',
    'ResourceType',
    'Resource',
    'ResourceEventChange',
]


class BaseModelMixin:

    def save(self, *args, **kwargs):
        """Update updated field and Call :meth:`full_clean` before saving."""

        if not self._state.adding:
            self.updated = timezone.now()

        self.full_clean()

        super().save(*args, **kwargs)

    def to_dict(self, fields=None, exclude=None):
        return utils.model_instance_to_dict(self, fields, exclude)

class BaseModel(BaseModelMixin, models.Model):
    """Base for all MCE models"""

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

"""
Model Settings:
    SettingsApp (1 par Site)
        Options global
    SettingsCompany (1 par Company)
        Options par Company
    SettingsSubscription (1 par Souscription)
        Options par Subscription

"""

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

    class Meta:
        ordering = ['name']


class Region(BaseModel):

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    # us-east-1
    name = models.CharField(max_length=255, db_index=True)

    slug = AutoSlugField(populate_from=['name'], overwrite=True, unique=False)

    display_name = models.CharField(max_length=255, db_index=True)

    longitude = models.FloatField(null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['provider', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "name"],
                name='provider_name_uniq',
            )
        ]


class ResourceType(BaseModel):

    # TODO: icon field ?

    # TODO: manque display name ou dans Description ?
    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(
                            max_length=1024,
                            populate_from=['name'],
                            overwrite=True,
                            unique=True)

    description = models.CharField(max_length=255, null=True, blank=True)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    # Déplacer dans profil qui aura un ManyToMany vers les resources désactivé pour sync?
    exclude_sync = models.BooleanField(default=False)

    tags = TaggableManager()

    @property
    def provider_name(self):
        return self.provider.name

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data["tags"] = self.tags.slugs() #[tag for tag in self.tags.all()]
        return data

    def __str__(self):
        return f"{self.provider.name} - {self.name}"

    class Meta:
        ordering = ['provider', 'name']


class SyncSettings(BaseModel):

    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(populate_from=['name'], overwrite=True, unique=True)

    # TODO: clean field pour valider unique si True
    is_global = models.BooleanField(default=False)

    # TODO: en déplaçant champs dans InventorySetting, réutilisable dans Subscription et autres ?
    inventory_mode = models.CharField(
        max_length=20,
        choices=constants.InventoryMode.choices,
        default=constants.InventoryMode.PULL
    )

    delete_mode = models.CharField(
        max_length=20,
        choices=constants.DeleteMode.choices,
        default=constants.DeleteMode.DISABLE
    )

    include_providers = models.ManyToManyField(Provider, related_name="syncsettings_include")
    exclude_providers = models.ManyToManyField(Provider, related_name="syncsettings_exclude")

    include_regions = models.ManyToManyField(Region, related_name="syncsettings_include")
    exclude_regions = models.ManyToManyField(Region, related_name="syncsettings_exclude")

    include_resource_types = models.ManyToManyField(ResourceType, related_name="syncsettings_include")
    exclude_resource_types = models.ManyToManyField(ResourceType, related_name="syncsettings_exclude")

    class Meta:
        ordering = ['name']
        verbose_name = _("Synchronization Settings")
        verbose_name_plural = _("Synchronization SyncSettings")

    def __str__(self):
        return self.name


class Company(BaseModel):

    # TODO: Settings: timeout, retry, wait interval, tag filters...

    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(populate_from=['name'], overwrite=True, unique=True)

    settings = models.ForeignKey(SyncSettings, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['name']
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

# TODO: renommer en ResourceTag !
class Tag(BaseModel):
    """Cloud Tags"""

    name = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)

    value = models.CharField(max_length=1024)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    @property
    def provider_name(self):
        return self.provider.name

    @property
    def company_name(self):
        return self.company.name

    def to_dict(self, fields=None, exclude=[]):
        data = super().to_dict(fields=fields, exclude=exclude)

        if self.provider:
            data["provider"] = self.provider.name

        if self.company:
            data["company"] = self.company.name

        return data

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "provider", "name", "value"],
                name='company_provider_name_value_uniq',
                #condition=models.Q(provider__isnull=False, company__isnull=False),
            ),
        ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Resource(BaseModel):
    """Generic Resource"""

    # max 286 sur Azure
    resource_id = models.CharField(unique=True, max_length=1024)

    slug = AutoSlugField(max_length=1024, populate_from=['resource_id'], 
                        slugify_function=utils.slugify_resource_id_function, 
                        overwrite=True, unique=True)

    name = models.CharField(max_length=255)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    # TODO: limit choices same provider
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # TODO: limit choices same provider
    tags = models.ManyToManyField(Tag)

    metas = JSONField(default=dict, null=True, blank=True)

    #changes = GenericRelation('ResourceEventChange', related_query_name='resource')

    locked = models.BooleanField(default=False, editable=False)

    active = models.BooleanField(default=True, editable=False)

    #categories = TaggableManager()

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
        #exclude.append("changes")
        exclude.append("resource_ptr")
        # exclude.append("tagged_items")
        # exclude.append("categories")
        data = super().to_dict(fields=fields, exclude=exclude)

        data['resource_type'] = self.resource_type.name
        data['company'] = self.company.name
        data['provider'] = str(self.provider.name)
        # data["categories"] = [item for item in self.categories.slugs()]

        data["tags"] = [tag.to_dict(fields=["name", "value", "provider"]) for tag in self.tags.all()]

        return data

    class Meta:
        ordering = ['name']


class ResourceEventChange(BaseModel):

    # TODO: state: new|sended|consumed

    # TODO: ne pas utiliser ContentType, lien par id ou resource_id sans clé

    action = models.CharField(max_length=10, choices=constants.EventChangeType.choices)

    changes = JSONField(default=list, null=True, blank=True)

    old_object = JSONField(default=dict, null=True, blank=True)

    new_object = JSONField(default=dict, null=True, blank=True)

    diff = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()

    # TODO: on_delete=models.SET_NULL, null=True)
    content_object = GenericForeignKey(
        'content_type', 'object_id', for_concrete_model=True
    )

    def to_dict(self, fields=None, exclude=None):
        data = super().to_dict(fields=fields, exclude=exclude)
        data["content_type"] = {
            "app_label": self.content_type.app_label,
            "model": self.content_type.model,
            "name": self.content_type.name,
            "id": self.object_id
        }
        return data

    # def to_json(self, fields=None, exclude=None):
    #     #from django.core import serializers
    #     data = self.to_dict(fields=fields, exclude=exclude)
    #     #json.dumps(data, cls=DjangoJSONEncoder, indent=4)

    @classmethod
    def create_event_change_update(cls, old_obj, new_obj, resource):
        """UPDATE Event for Resource

        TODO: déplacer sous forme de signal en 2 phase: pre_save et post_save
        - pre_save, remplit tout sauf new_object, changes et diff
        - post_save, remplit le reste
        """
        if getattr(settings, "MCE_CHANGES_ENABLE", False) is False:
            return

        patch = jsonpatch.JsonPatch.from_diff(old_obj, new_obj)

        if patch.patch:
            return cls.objects.create(
                action=constants.EventChangeType.UPDATE,
                content_object=resource,
                changes=list(patch),
                old_object=old_obj,
                new_object=new_obj,
                diff=None,
            )

    @classmethod
    def create_event_change_delete(cls, queryset):
        """DELETE Event for ResourceAzure and ResourceGroupAzure"""

        for doc in queryset:
            cls.objects.create(
                action=constants.EventChangeType.DELETE,
                content_object=doc,
                old_object=doc.to_dict(exclude=['created', 'updated', 'tagged_items']),
            )

    def __str__(self):
        return f"{self.content_type.app_label}.{self.content_type.model}: {self.object_id}"

    class Meta:
        ordering = ['-created', 'object_id']


#@receiver(post_save, sender=Company)
def create_default_groups_for_new_company(sender, instance=None, created=None, **kwargs):
    """Create default Groups for new Company
    
    Args:
        sender: 
        instance: 
        created: 
        **kwargs: 

    Returns:

    """
    if not created:
        return

    if instance.owner_group and instance.user_group:
        return

    group_name = f"{instance.slug.replace('-', '_')}_Admins"
    admins, created = Group.objects.get_or_create(name=group_name)

    """
    # TODO: perms for admin group
    # add_company
    # change_company
    # delete_company
    # view_company
    assign_perm(perm, admins, obj=instance)
    """

    group_name = f"{instance.slug.replace('-', '_')}_Users"
    users, created = Group.objects.get_or_create(name=group_name)
    # TODO: perms for user group

    instance.owner_group = admins
    instance.user_group = users
    instance.save()



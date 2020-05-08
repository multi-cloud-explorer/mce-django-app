from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django_cryptography.fields import encrypt
from django_extensions.db.fields import AutoSlugField
from jsonfield import JSONField

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app import signals

from .common import BaseModel, Resource, Company, ResourceEventChange

__all__ = [
    'Vcenter',
    'DatacenterVMware',
    'ResourceVMware',
    #'ResourceVMwareVM'
]

# Un vcenter est aussi une Resource  ?
# TODO: prévoir auth par cert ssl
class Vcenter(BaseModel):

    # TODO: extraire name de l'url si non fournie
    name = models.CharField(max_length=255, unique=True)

    slug = AutoSlugField(max_length=1024, populate_from=['name'],
                        slugify_function=utils.slugify_resource_id_function,
                        overwrite=True, unique=True)

    company = models.ForeignKey(
        Company, on_delete=models.PROTECT,
    )

    # FIXME: encrypt(
    url = models.URLField(
        max_length=1024,
        unique=True,
        help_text=_("Full URL with options. Ex: https://host?username=user&password=pass")
    )

    @property
    def company_name(self):
        return self.company.name

    def get_auth(self):
        """Auth format for `mce_lib_vsphere.core.Client`"""
        return self.url

    class Meta:
        verbose_name = _("VMware Vcenter")
        verbose_name_plural = _("VMware Vcenters")

class DatacenterVMware(Resource):

    vcenter = models.ForeignKey(
        Vcenter, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["vcenter", "name"], name='vcenter_name_uniq'
    #         ),
    #     ]
    @property
    def vcenter_name(self):
        return self.vcenter.name

    class Meta:
        verbose_name = _("VMware Datacenter")
        verbose_name_plural = _("VMware Datacenters")

class ResourceVMware(Resource):

    datacenter = models.ForeignKey(DatacenterVMware, on_delete=models.CASCADE)

    def to_dict(self, fields=None, exclude=[]):
        data = super().to_dict(fields=fields, exclude=exclude)
        data["datacenter"] = self.datacenter.to_dict(fields=fields, exclude=exclude)
        return data

    @property
    def vcenter_name(self):
        return self.datacenter.vcenter_name

    @property
    def datacenter_name(self):
        return self.datacenter.name

    class Meta:
        verbose_name = _("VMware Resource")
        verbose_name_plural = _("VMware Resources")

# TODO: hériter directement de Resource ?
# class ResourceVMwareVM(ResourceVMware):
#
#     is_template = models.BooleanField(default=False)
#
#     # "powerState": "poweredOn",
#     # TODO: choices
#     power_state = models.CharField(max_length=255, null=True, blank=True)
#
#     guest_state = models.CharField(max_length=255, null=True, blank=True)
#
#     cpu = models.IntegerField(default=0, null=True, blank=True)
#
#     # TODO: disk size / free
#
#     # en MB
#     memory = models.IntegerField(default=0, null=True, blank=True)
#
#     dns_name = models.CharField(max_length=255, null=True, blank=True)
#
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#
#     resource_pool = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
#
#     vmx_path = models.CharField(max_length=255, null=True, blank=True)
#
#     os_name = models.CharField(max_length=255, null=True, blank=True)
#

if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceVMware)
    def resource_vmware_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)


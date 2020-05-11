from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django_cryptography.fields import encrypt
from jsonfield import JSONField

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app import signals

from mce_django_app.models.common import BaseModel, Resource, Company, Provider

"""
from mptt.models import MPTTModel, TreeForeignKey

class FolderGCP(BaseModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.PROTECT)

    class MPTTMeta:
        #order_insertion_by = ['position']
        parent_attr = 'parent'
"""

class ProjectGCP(BaseModel):
    """GCP Project Model"""

    # name: str
    # full_name: str
    # labels: {}
    # number (char)
    # parent: dict
    # status: text (ACTIVE|...)
    # path:  /projects/mce-labo
    # project_id = str = 'mce-labo'
    # scopes ?

    name = models.CharField(max_length=255)

    project_id = models.CharField(max_length=255, unique=True, verbose_name=_("Project ID"))

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss"
    )

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)

    credentials = JSONField(default={}, null=True, blank=True)

    def get_auth(self):
        """Auth format for `mce_lib_gcp.???`"""

        data = dict(
            project_id=self.project_id,
            credentials=self.credentials,
        )
        return data

    class Meta:
        verbose_name = _("GCP Project")
        verbose_name_plural = _("GCP Projects")


class ResourceGCP(Resource):

    project = models.ForeignKey(ProjectGCP, on_delete=models.PROTECT)

    @property
    def project_name(self):
        return self.project.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("GCP Project")
        verbose_name_plural = _("GCP Projects")


if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceGCP)
    def resource_gcp_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)

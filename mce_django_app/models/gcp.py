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

from mce_django_app.models.common import BaseModel, Resource, BaseSubscription

class ProjectGCP(BaseModel):
    """GCP Project Model"""

    # labels
    # number (char)
    # parent: dict
    # status: text (ACTIVE|...)
    # full_name
    # path:  /projects/mce-labo
    # project_id = str = mce-labo
    # scopes ?

    project_id = models.CharField(max_length=255, verbose_name=_("Project ID"))

    credentials = encrypt(JSONField(default={}, null=True, blank=True))

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

class ResourceGCP(Resource):

    project = models.ForeignKey(ProjectGCP, on_delete=models.PROTECT)

    # datacenter ?

if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceGCP)
    def resource_gcp_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)

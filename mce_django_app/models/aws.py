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

"""
Regions:
ec2 = boto3.client('ec2')
response = ec2.describe_regions()
print('Regions:', response['Regions'])

[{'Endpoint': 'ec2.eu-north-1.amazonaws.com',
  'RegionName': 'eu-north-1',
  'OptInStatus': 'opt-in-not-required'},
 {'Endpoint': 'ec2.ap-south-1.amazonaws.com',
  'RegionName': 'ap-south-1',
  'OptInStatus': 'opt-in-not-required'},
  ...]

"""


class SubscriptionAWS(BaseSubscription):
    """AWS Subscription Model"""

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


class ResourceAWS(Resource):

    # location/zone/region
    # kind ?
    # TODO: tenant / region ?

    # ID: arn
    # arn:aws:ec2:us-east-1:000000000000:instance/i-8d96dc48b01fedd67
    # arn:aws:s3:::my-tf-test-bucket: !!! Attention, pas de subscription ID ?

    """
    "Location": "eu-west-1",

    'InstanceId': 'i-8d96dc48b01fedd67',
    'ImageId': 'ami-045fa58af83eb0ff4',
    'InstanceType': 't2.micro',    

    'PrivateDnsName': 'ip-10-32-137-102.ec2.internal',
    'PrivateIpAddress': '10.32.137.102',

    'PublicDnsName': 'ec2-54-214-91-63.compute-1.amazonaws.com',
    'PublicIpAddress': '54.214.91.63',

    'State': {'Code': 16, 'Name': 'running'},
        0 : pending
        16 : running
        32 : shutting-down
        48 : terminated
        64 : stopping
        80 : stopped

    'StateReason': {'Code': None, 'Message': None},
    'StateTransitionReason': None,
    """

    subscription = models.ForeignKey(SubscriptionAWS, on_delete=models.PROTECT)

if getattr(settings, "MCE_CHANGES_ENABLE", False):

    @receiver(post_save, sender=ResourceAWS)
    def resource_aws_create_event_change(sender, instance=None, created=None, **kwargs):
        signals.create_event_change(sender, instance=instance, created=created, **kwargs)

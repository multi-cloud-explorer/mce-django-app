from django.db import models
from django.utils.translation import ugettext_lazy as _

from mce_django_app import utils
from mce_django_app import constants
from mce_django_app.models.common import BaseModel, Resource, GenericAccount, BaseSubscription

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

    # TODO: delegation role


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

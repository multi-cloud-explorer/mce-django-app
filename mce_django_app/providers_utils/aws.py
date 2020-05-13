import logging
from typing import Dict, List

import boto3
from boto3.session import Session as BotoSession

from django.conf import settings

from mce_lib_aws import SERVICES
from mce_lib_aws.crawler import get_selected_regions_and_services, get_all_assets

from mce_django_app import constants
from mce_django_app.exceptions import *
from mce_django_app.models.common import Provider, ResourceType, Region, ResourceEventChange, Tag
from mce_django_app.models import aws as models

logger = logging.getLogger(__name__)

MCE_CHANGES_ENABLE = getattr(settings, "MCE_CHANGES_ENABLE", False)

class FetchResourceError(Exception):
    pass

# https://github.com/boto/botocore/blob/master/botocore/data/endpoints.json

def sync_regions() -> Dict:
    """AWS Region Sync"""

    _created = 0
    _updated = 0

    provider = Provider.objects.get(name=constants.Provider.AWS)

    for region in list(get_selected_regions_and_services().keys()):
        _, created = Region.objects.get_or_create(
            name=region, provider=provider,
            defaults=dict(
                display_name=region,
            )
        )

        if created:
            _created += 1
        else:
            _updated += 1

    logger.info(f"sync - aws - Region - created[{_created}]- updated[{_updated}]")

    return dict(errors=0, created=_created, updated=_updated, deleted=0)


def sync_resource_type() -> Dict:
    """AWS ResourceType Sync"""

    _created = 0
    _updated = 0

    provider = Provider.objects.get(name=constants.Provider.AWS)

    for i, k in enumerate(list(SERVICES.keys()), start=1):

        logger.debug(f"{i} - create or update resource type [{k}]")

        _, created = ResourceType.objects.get_or_create(
            name=k, defaults=dict(provider=provider)
        )

        if created:
            _created += 1
        else:
            _updated += 1

    logger.info(f"sync - aws - ResourceType - created[{_created}]- updated[{_updated}]")

    return dict(errors=0, created=_created, updated=_updated, deleted=0)

def get_subscription_and_session(subscription_id: str):
    """

    Args:
        subscription_id:

    Returns:
        (models.SubscriptionAWS, boto3.session.Session)

    """
    # TODO: raise if active=False
    subscription = models.SubscriptionAWS.objects.get(subscription_id=subscription_id)
    auth = subscription.get_auth()
    session = boto3.Session(**auth)
    #session = cli.get_session(token=token['access_token'])
    return subscription, session


def sync_resource(
        resource: Dict = None,
        subscription_id: str = None,
        resource_id: str = None,
        resource_type: str = None,
        region: Region = None,
        subscription: models.SubscriptionAWS = None,
        session: BotoSession = None,
        disable_changes: bool = False) -> Dict:
    """Synchronize a `models.ResourceAWS` with database.

    Args:
        resource:
        subscription_id:
        resource_id:
        resource_group:
        resource_type:
        subscription:
        session:

    Returns:
        Dict: Return Pk and created is True|False and changes dict.

    """

    if not resource:
        if not resource_id:
            raise AttributeError("requires value: resource_id or resource")
        if not resource_type:
            raise AttributeError("requires value: resource_type or resource")

    provider = Provider.objects.filter(name=constants.Provider.AWS).first()
    if not provider:
        raise ProviderNotFound(f"Provider not found : {constants.Provider.AWS}")

    if resource and not resource_id:
        resource_id = resource['arn']

    # if resource and resource_id and not subscription_id:
    #     subscription_id = resource_id.split('/')[4]

    if not subscription or not session:
        subscription, session = get_subscription_and_session(subscription_id)

    company = subscription.company

    if resource and not resource_type:
        resource_type = resource['service']

    logger.debug(f"start for resource [{resource_id}]")

    _type = ResourceType.objects.filter(name__iexact=resource_type, provider=provider).first()

    if not _type:
        msg = f"resource type [{resource_type}] not found - resource [{resource_id}]"
        logger.error(msg)
        raise ResourceTypeNotFound(msg)

    if _type.exclude_sync:
        msg = f"resource type [{resource_type}] disabled for synchronize - resource [{resource_id}]"
        logger.error(msg)
        raise DisableSyncError(msg)

    # if not resource:
    #     try:
    #         resource = cli.get_resource_by_id(resource_id, session=session)
    #     except Exception as err:
    #         msg = f"fetch resource {resource_id} error : {err}"
    #         logger.exception(msg)
    #         raise FetchResourceError(msg)

    if not region:
        region = Region.objects.filter(name=resource['region'], provider=provider).first()
        if not region:
            msg = f"region not found [{resource['region']}] - bypass resource [{resource_id}]"
            raise RegionNotFound(msg)

    metas = resource.get('data', {}) or {}

    tags_objects = []

    """
    "arn": "arn:aws:s3:::mybucket0",
    "data": {
      "Name": "mybucket0",
      "CreationDate": "2020-05-12T14:00:53.127747"
    },
    "tags": {
      "key1": "value1"
    },
    "name": "mybucket0",
    "account_id": "123456789001",
    "region": "us-east-1",
    "service": "aws.s3.bucket"
    
    """
    datas = dict(
        name=resource['name'],
        subscription=subscription,
        company=company,
        resource_type=_type,
        region=region,
        provider=provider,
        metas=metas,
    )

    tags = resource.get('tags', {}) or {}
    for k, v in tags.items():
        tag, created = Tag.objects.update_or_create(
            name=k, company=company, provider=provider, value=v
        )
        tags_objects.append(tag)
        # if created: todo event tag

    old_resource = models.ResourceAWS.objects.filter(resource_id=resource_id).first()
    old_object = None
    if old_resource:
        old_object = old_resource.to_dict(exclude=["created", "updated"])

    new_resource, created = models.ResourceAWS.objects.update_or_create(
        resource_id=resource_id, defaults=datas
    )

    if tags_objects:
        new_resource.tags.set(tags_objects)

    result = {"pk": new_resource.pk, "created": created, "changes": None}

    if not disable_changes and getattr(settings, "MCE_CHANGES_ENABLE", False):
        changes = None

        if not created:
            new_object = new_resource.to_dict(exclude=["created", "updated", "tagged_items"])
            changes = ResourceEventChange.create_event_change_update(old_object, new_object, new_resource)

        if changes:
            result["changes"] = changes.to_dict(exclude=['created', 'updated', 'tagged_items'])

    return result


def sync_resource_list(
        subscription_id: str = None,
        resources: List = None,
        subscription: models.SubscriptionAWS = None,
        session: BotoSession = None,
        disable_changes: bool = False,
        disable_delete: bool = False) -> Dict:

    provider = Provider.objects.filter(name=constants.Provider.AWS).first()
    if not provider:
        raise ProviderNotFound(f"Provider not found : {constants.Provider.AWS}")

    if subscription_id and not subscription:
        raise  AttributeError("subscription_id or subscription is require")

    if not subscription or not session:
        # TODO: catch error
        subscription, session = get_subscription_and_session(subscription_id)

    company = subscription.company

    _created = 0
    _updated = 0
    _errors = 0
    _deleted = 0

    found_ids = []
    regions = {}

    if not resources:
        print("!!!!!!!!!!!! NOT RESOURCE")
        resources_allowed = [resource.name for resource in company.resource_types.all()]
        regions_allowed = [region.name for region in company.regions.all()]
        resources = get_all_assets(session, subscription_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed)

    for i, resource in enumerate(resources):

        is_complete = False
        if "data" in resource:
            is_complete = True

        resource_id = resource['arn']
        found_ids.append(resource_id)
        location = resource['region']
        logger.debug(f"{i} - create or update azure resource [{resource_id}]")

        # --- Region
        if location in regions:
            region = regions[location]
        else:
            region = Region.objects.filter(name=location, provider=provider).first()

        if not region:
            _errors += 1
            msg = f"region not found [{location}] - bypass resource [{resource_id}]"
            logger.error(msg)
            continue

        if not region.name in regions:
            regions[region.name] = region

        try:
            result = sync_resource(
                subscription_id=subscription_id,
                resource=resource if is_complete else None,
                resource_id=resource_id,
                resource_type=resource.get('type'),
                subscription=subscription,
                region=region,
                session=session,
                disable_changes=disable_changes
            )
            if result["created"]:
                _created += 1
            else:
                _updated += 1
        except Exception as err:
            _errors += 1
            logger.error(f"sync resource error: {str(err)}")
            continue

    if not disable_delete:
        # Create events delete
        qs = models.ResourceAWS.objects.exclude(
            resource_id__in=found_ids, subscription=subscription
        )
        if not disable_changes and getattr(settings, "MCE_CHANGES_ENABLE", False):
            ResourceEventChange.create_event_change_delete(qs)

        qs = models.ResourceAWS.objects.exclude(
            resource_id__in=found_ids, subscription=subscription
        )
        _deleted, objects = qs.delete()

        logger.info("[%s] old ResourceAWS deleted" % _deleted)

    return dict(errors=_errors, created=_created, updated=_updated, deleted=_deleted)

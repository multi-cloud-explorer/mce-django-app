import logging
from typing import Dict, List

import requests
from django.conf import settings

from mce_azure.utils import get_access_token
from mce_azure import core as cli

from mce_azure.core import PROVIDERS
from mce_azure import regions

from mce_django_app import constants
from mce_django_app.exceptions import *
from mce_django_app.models.common import Provider, ResourceType, Region, ResourceEventChange, Tag
from mce_django_app.models import azure as models

logger = logging.getLogger(__name__)

MCE_CHANGES_ENABLE = getattr(settings, "MCE_CHANGES_ENABLE", False)

class ResourceGroupNotFound(Exception):
    pass

class FetchResourceError(Exception):
    pass

def sync_regions() -> Dict:
    """Azure Region Sync"""

    _created = 0
    _updated = 0

    provider = Provider.objects.get(name=constants.Provider.AZURE)

    for region in regions.get_regions():
        _, created = Region.objects.get_or_create(
            name=region['name'], provider=provider,
            defaults=dict(
                display_name=region.get('displayName'),
                longitude=float(region.get('longitude')),
                latitude=float(region.get('latitude'))
            )
        )

        if created:
            _created += 1
        else:
            _updated += 1

    logger.info(f"sync - azure - Region - created[{_created}]- updated[{_updated}]")

    return dict(errors=0, created=_created, updated=_updated, deleted=0)

def sync_resource_type(max_limit: int = None) -> Dict:
    """Azure ResourceType Sync"""

    _created = 0
    _updated = 0

    provider = Provider.objects.get(name=constants.Provider.AZURE)

    for i, (k, v) in enumerate(PROVIDERS.items(), start=1):
        if max_limit and i > max_limit:
            break

        logger.debug(f"{i} - create or update resource type [{k}]")

        _, created = ResourceType.objects.get_or_create(
            name=k, defaults=dict(provider=provider)
        )

        if created:
            _created += 1
        else:
            _updated += 1

    logger.info(f"sync - azure - ResourceType - created[{_created}]- updated[{_updated}]")

    return dict(errors=0, created=_created, updated=_updated, deleted=0)

def get_subscription_and_session(subscription_id: str):
    """

    Args:
        subscription_id:

    Returns:
        (models.SubscriptionAzure, requests.Session)

    """
    # TODO: raise if active=False
    subscription = models.SubscriptionAzure.objects.get(subscription_id=subscription_id)
    auth = subscription.get_auth()
    token = get_access_token(**auth)
    session = cli.get_session(token=token['access_token'])
    return subscription, session

def sync_resource_group(subscription_id: str, resources_groups: List = None, max_error: int = None, disable_changes: bool = False) -> Dict:

    # TODO: catch error
    subscription, session = get_subscription_and_session(subscription_id)
    company = subscription.company
    provider = Provider.objects.get(name=constants.Provider.AZURE)

    # TODO: catch error
    if not resources_groups:
        resources_groups = cli.get_resourcegroups_list(subscription_id, session=session)

    _created = 0
    _updated = 0
    _errors = 0
    _deleted = 0

    found_ids = []

    RESOURCE_GROUP_TYPE = "Microsoft.Resources/resourceGroups".lower()

    _type = ResourceType.objects.get(name__iexact=RESOURCE_GROUP_TYPE)

    for r in resources_groups:

        resource_id = r['id'].lower()
        found_ids.append(resource_id)

        region = Region.objects.filter(name=r['location'], provider=provider).first()
        if not region:
            _errors += 1
            msg = f"region not found [{r['location']}] - bypass resource [{resource_id}]"
            logger.error(msg)
            continue

        if r['type'].lower() != RESOURCE_GROUP_TYPE:
            _errors += 1
            msg = f"bad resource type [{r['type']}] - bypass resource [{resource_id}]"
            logger.error(msg)
            continue

        if max_error and _errors >= max_error:
            raise Exception("MAX ERROR...")

        # TODO: ajouter autres champs ?
        metas = r.get('properties', {})
        print('!!! sources metas : ', metas)
        assert isinstance(metas, dict) is True

        tags_objects = []

        # TODO: events et logs
        tags = r.get('tags', {}) or {}
        for k, v in tags.items():
            tag, created = Tag.objects.update_or_create(
                name=k, company=company, provider=provider, value=v
            )
            tags_objects.append(tag)
            # if created: todo event tag

        old_resource = models.ResourceAzure.objects.filter(resource_id=resource_id).first()

        old_object = None

        if old_resource:
            old_object = old_resource.to_dict(exclude=["created", "updated"])

        new_resource, created = models.ResourceAzure.objects.update_or_create(
            resource_id=resource_id,
            defaults=dict(
                name=r['name'],  # TODO: lower ?
                subscription=subscription,
                company=company,
                resource_type=_type,
                #location=r['location'],
                region=region,
                provider=provider,
                metas=metas,
            )
        )
        #new_resource.metas = metas
        #new_resource.save()
        #new_resource.refresh_from_db()
        if tags_objects:
            new_resource.tags.set(tags_objects)

        if created:
            _created += 1
        elif not disable_changes and getattr(settings, "MCE_CHANGES_ENABLE", False):
            new_object = new_resource.to_dict(exclude=["created", "updated", "tagged_items"])
            #print('!!! old, new, equal : ', type(old_object['metas']), type(new_object['metas']), old_object['metas']==new_object['metas'])
            changes = ResourceEventChange.create_event_change_update(old_object, new_object, new_resource)
            if changes:
                _updated += 1

    logger.info(
        "sync - azure - ResourceAzure - _errors[%s] - created[%s]- updated[%s]"
        % (_errors, _created, _updated)
    )

    # Create events delete
    qs = models.ResourceAzure.objects.exclude(
        resource_id__in=found_ids, subscription=subscription
    )
    # TODO: CHANGES_MODES: CREATE/UPDATE/DELETE
    if not disable_changes and getattr(settings, "MCE_CHANGES_ENABLE", False):
        ResourceEventChange.create_event_change_delete(qs)

    # Mark for deleted
    # TODO: delegate tasks ?
    _deleted, objects = models.ResourceAzure.objects.exclude(
        resource_id__in=found_ids, subscription=subscription
    ).delete()

    logger.info(f"mark for deleted. [{_deleted}] old ResourceAzure")

    return dict(errors=_errors, created=_created, updated=_updated, deleted=_deleted)

def sync_resource(
        resource: Dict = None,
        subscription_id: str = None,
        resource_id: str = None,
        resource_group: models.ResourceAzure = None,
        resource_type: str = None,
        region: Region = None,
        subscription: models.SubscriptionAzure = None,
        session: requests.Session = None,
        disable_changes: bool = False) -> Dict:
    """Synchronize a `models.ResourceAzure` with database.

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

    provider = Provider.objects.filter(name=constants.Provider.AZURE).first()
    if not provider:
        raise ProviderNotFound(f"Provider not found : {constants.Provider.AZURE}")

    if resource and not resource_id:
        resource_id = resource['id']

    if resource and resource_id and not subscription_id:
        subscription_id = resource_id.split('/')[4]

    # TODO: récupérer le token de session ?: session.headers.get('authorization')
    # TODO: exception
    if not subscription or not session:
        subscription, session = get_subscription_and_session(subscription_id)

    company = subscription.company

    if resource and not resource_type:
        resource_type = resource['type']

    logger.debug(f"start for resource [{resource_id}]")

    if '|' in resource_type:
        resource_type = resource_type.split('|')[0]

    _type = ResourceType.objects.filter(name__iexact=resource_type, provider=provider).first()

    if not _type:
        msg = f"resource type [{resource_type}] not found - resource [{resource_id}]"
        logger.error(msg)
        raise ResourceTypeNotFound(msg)

    if _type.exclude_sync:
        msg = f"resource type [{resource_type}] disabled for synchronize - resource [{resource_id}]"
        logger.error(msg)
        raise DisableSyncError(msg)

    if not resource_group:
        group_name = resource_id.split('/')[4]
        group_id = f"/subscriptions/{subscription.subscription_id}/resourceGroups/{group_name}"
        resource_group = models.ResourceAzure.objects.filter(
            resource_id__iexact=group_id,
            company=company,
            subscription=subscription
        ).first()

    if not resource_group:
        msg = f"resource group [{group_id}] not found - resource [{resource_id}]"
        logger.error(msg)
        raise ResourceGroupNotFound(msg)

    if not resource:
        try:
            resource = cli.get_resource_by_id(resource_id, session=session)
        except Exception as err:
            msg = f"fetch resource {resource_id} error : {err}"
            logger.exception(msg)
            raise FetchResourceError(msg)

    if not region:
        region = Region.objects.filter(name=resource['location'], provider=provider).first()
        if not region:
            msg = f"region not found [{resource['location']}] - bypass resource [{resource_id}]"
            raise RegionNotFound(msg)

    metas = resource.get('properties', {}) or {}

    tags_objects = []

    datas = dict(
        name=resource['name'],
        subscription=subscription,
        company=company,
        resource_type=_type,
        region=region,
        provider=provider,
        resource_group=resource_group,
        metas=metas,
    )

    if resource.get('sku'):
        datas['sku'] = resource.get('sku')

    if resource.get('kind'):
        datas['kind'] = resource.get('kind')

    if resource.get('plan'):
        datas['plan'] = resource.get('plan')

    if resource.get('managed_by'):
        datas['managed_by'] = resource.get('managed_by')

    tags = resource.get('tags', {}) or {}
    for k, v in tags.items():
        tag, created = Tag.objects.update_or_create(
            name=k, company=company, provider=provider, value=v
        )
        tags_objects.append(tag)
        # if created: todo event tag

    old_resource = models.ResourceAzure.objects.filter(resource_id=resource_id).first()
    old_object = None
    if old_resource:
        old_object = old_resource.to_dict(exclude=["created", "updated"])

    new_resource, created = models.ResourceAzure.objects.update_or_create(
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
        subscription: models.SubscriptionAzure = None,
        session: requests.Session = None,
        disable_changes: bool = False,
        disable_delete: bool = False) -> Dict:

    provider = Provider.objects.filter(name=constants.Provider.AZURE).first()
    if not provider:
        raise ProviderNotFound(f"Provider not found : {constants.Provider.AZURE}")

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
    resource_groups = {}

    if not resources:
        resources = cli.get_resources_list(subscription_id, session)

    for i, resource in enumerate(resources):

        is_complete = False
        if "properties" in resource:
            is_complete = True

        resource_id = resource['id']
        found_ids.append(resource_id)
        location = resource['location']
        logger.debug(f"{i} - create or update azure resource [{resource_id}]")

        # --- Region
        if location in regions:
            region = regions[location]
        else:
            region = Region.objects.filter(name=resource['location'], provider=provider).first()

        if not region:
            _errors += 1
            msg = f"region not found [{resource['location']}] - bypass resource [{resource_id}]"
            logger.error(msg)
            continue

        if not region.name in regions:
            regions[region.name] = region

        # --- ResourceGroup
        group_name = resource_id.split('/')[4]
        group_id = f"/subscriptions/{subscription.subscription_id}/resourceGroups/{group_name}"

        if group_id in resource_groups:
            resource_group = resource_groups[group_id]
        else:
            resource_group = models.ResourceAzure.objects.filter(
                resource_id__iexact=group_id,
                company=company,
                subscription=subscription
            ).first()

        if not resource_group:
            _errors += 1
            msg = f"resource group [{group_id}] not found - resource [{resource_id}]"
            logger.error(msg)
            continue

        if not group_id in resource_groups:
            resource_groups[group_id] = resource_group

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
        qs = models.ResourceAzure.objects.exclude(
            resource_id__in=found_ids, subscription=subscription
        )
        if not disable_changes and getattr(settings, "MCE_CHANGES_ENABLE", False):
            ResourceEventChange.create_event_change_delete(qs)

        qs = models.ResourceAzure.objects.exclude(
            resource_id__in=found_ids, subscription=subscription
        )
        _deleted, objects = qs.delete()

        logger.info("[%s] old ResourceAzure deleted" % _deleted)

    return dict(errors=_errors, created=_created, updated=_updated, deleted=_deleted)

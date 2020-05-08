import logging
from typing import Dict

from mce_lib_vsphere.core import ResourceTypes

from mce_django_app import constants
from mce_django_app.models.common import Provider, ResourceType

logger = logging.getLogger(__name__)

def sync_resource_type() -> Dict:
    """Vsphere ResourceType Sync"""

    _created = 0
    _updated = 0

    provider, _ = Provider.objects.get_or_create(name=constants.Provider.VMWARE)

    for resource in ResourceTypes:
        name = resource.value.lower()
        r, created = ResourceType.objects.get_or_create(name=name, defaults=dict(provider=provider))
        if created:
            _created += 1
        else:
            _updated += 1

    logger.info(f"sync - vsphere - ResourceType - created[{_created}]- updated[{_updated}]")

    return dict(errors=0, created=_created, updated=_updated, deleted=0)

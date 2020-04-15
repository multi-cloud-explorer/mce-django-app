from uuid import uuid4

import pytest
from ddf import G

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app.models.common import GenericAccount, Tag, ResourceType
from mce_django_app import constants
from mce_django_app.models import azure as models

@pytest.fixture
def resource_type():
    return ResourceType.objects.create(
        name="Microsoft.Compute/virtualMachines",
        description="Azure VirtualMachines",
        provider=constants.Provider.AZURE
    )

@pytest.fixture
def tags():
    return G(Tag, n=5)

@pytest.fixture
def generic_account():
    return G(GenericAccount)

@pytest.fixture
def subscription(generic_account):
    return models.Subscription.objects.create(
        id=uuid4(),
        name="sub1",
        tenant=uuid4(),
        location="francecentral",
        account=generic_account
    )

@pytest.fixture
def resource_group(subscription):

    resource_type = ResourceType.objects.create(
        name="Microsoft.Resources/resourceGroups",
        provider=constants.Provider.AZURE
    )
    
    name = "rg1"
    resource_id = f"/subscriptions/{subscription.pk}/resourceGroups/{name}/providers/{resource_type.name}/{name}"
    
    return models.ResourceGroupAzure.objects.create(
        id=resource_id,
        name=name,
        resource_type=resource_type,
        subscription=subscription,
        provider=constants.Provider.AZURE,
        location="francecentral",
    )


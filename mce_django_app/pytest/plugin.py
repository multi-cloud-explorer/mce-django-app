from uuid import uuid4
import pytest
from ddf import G, M
from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common
from mce_django_app.models import azure
from mce_django_app.models import account

"""
Microsoft.Resources/resourceGroups
Microsoft.ClassicCompute/virtualMachines
Microsoft.Sql/servers/databases
"""

def pytest_configure(config):
    config.addinivalue_line("markers", "mce_bug: mark test as known bug")

@pytest.fixture
def mce_app_company():
    return G(common.Company, name="my-company")

@pytest.fixture
def mce_app_user_with_company(mce_app_company):
    # Token
    return G(account.User, company=mce_app_company)

@pytest.fixture
def mce_app_user_without_company():
    # Token
    return G(account.User)

@pytest.fixture
def mce_app_resource_type():
    return G(common.ResourceType, 
        name="aws.ec2.instance",
        description="EC2 Instance",
        provider=constants.Provider.AWS
    )

@pytest.fixture
def mce_app_resource_type_aws(mce_app_resource_type):
    return mce_app_resource_type

@pytest.fixture
def mce_app_resource_type_azure():
    return G(common.ResourceType,
        name="Microsoft.ClassicCompute/virtualMachines",
        description="Azure VirtualMachine",
        provider=constants.Provider.AZURE
    )

@pytest.fixture
def mce_app_resource_type_azure_group():
    return G(common.ResourceType, 
        name="Microsoft.Resources/resourceGroups",
        provider=constants.Provider.AZURE
    )


@pytest.fixture
def mce_app_resource_type_azure_vm(mce_app_resource_type_azure):
    return mce_app_resource_type_azure


@pytest.fixture
def mce_app_tags_five():
    return G(common.Tag, n=5)

@pytest.fixture
def mce_app_generic_account(mce_app_company):
    return G(common.GenericAccount, company=mce_app_company)

@pytest.fixture
def mce_app_resource(mce_app_resource_type, mce_app_company):
    """Return 1 Resource instance with 3 tags"""

    resource = G(common.Resource, 
        name="myname",
        resource_type=mce_app_resource_type,
        company=mce_app_company,
        provider=mce_app_resource_type.provider,
        tags=G(common.Tag, provider=mce_app_resource_type.provider, n=3)
    )

    return resource

@pytest.fixture
def mce_app_resource_list(mce_app_resource_type, mce_app_company):
    """Return 10 Resource instance with 3 tags"""

    return G(common.Resource,
        resource_type=mce_app_resource_type,
        provider=mce_app_resource_type.provider,
        company=mce_app_company,
        tags=G(common.Tag, provider=mce_app_resource_type.provider, n=3),
        n=10,
    )


# -- Azure

@pytest.fixture
def mce_app_subscription_azure(
    mce_app_generic_account,
    mce_app_company):

    return azure.SubscriptionAzure.objects.create(
        subscription_id=str(uuid4()),
        name="sub1",
        company=mce_app_company,
        tenant=str(uuid4()),
        location="francecentral",
        account=mce_app_generic_account
    )

@pytest.fixture
def mce_app_resource_group_azure(mce_app_company, mce_app_subscription_azure, mce_app_resource_type_azure):
    """Return 1 Azure Resource Group with ResourceGroup Type"""

    name = "rg1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.pk}/resourceGroups/{name}/providers/{mce_app_resource_type_azure.name}/{name}"
    
    return azure.ResourceGroupAzure.objects.create(
        resource_id=resource_id,
        name=name,
        resource_type=mce_app_resource_type_azure,
        company=mce_app_company,
        subscription=mce_app_subscription_azure,
        provider=constants.Provider.AZURE,
        location="francecentral",
    )


@pytest.fixture
def mce_app_resource_azure(
    mce_app_company, 
    mce_app_subscription_azure, 
    mce_app_resource_group_azure, 
    mce_app_resource_type_azure, 
    mce_app_tags_five):

    name = "vm1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.pk}/resourceGroups/{mce_app_resource_group_azure.name}/providers/{mce_app_resource_type_azure.name}/{name}"

    assert azure.ResourceAzure.objects.count() == 0

    resource = azure.ResourceAzure.objects.create( 
        resource_id=resource_id,
        name=name,
        resource_type=mce_app_resource_type_azure,
        company=mce_app_company,
        resource_group=mce_app_resource_group_azure,
        subscription=mce_app_subscription_azure,
        provider=constants.Provider.AZURE,
        location="francecentral",
        
    )
    resource.tags.set(mce_app_tags_five)
    return resource


from uuid import uuid4
import pytest
from ddf import G, M
from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common
from mce_django_app.models import azure
from mce_django_app.models import aws
from mce_django_app.models import account
from mce_django_app.models import gcp
from mce_django_app.models import vsphere

"""
Microsoft.Resources/resourceGroups
Microsoft.ClassicCompute/virtualMachines
Microsoft.Sql/servers/databases
"""

def pytest_configure(config):
    config.addinivalue_line("markers", "mce_known_bug: mark test as known bug")
    config.addinivalue_line("markers", "mce_todo: mark todo")

# --- common : Provider

@pytest.fixture
def mce_app_provider():
    return common.Provider.objects.create(
        name=constants.Provider.AZURE
    )

@pytest.fixture
def mce_app_provider_azure(mce_app_provider):
    return mce_app_provider

@pytest.fixture
def mce_app_provider_aws():
    return common.Provider.objects.create(
        name=constants.Provider.AWS
    )

@pytest.fixture
def mce_app_provider_gcp():
    return common.Provider.objects.create(
        name=constants.Provider.GCP
    )

@pytest.fixture
def mce_app_provider_vmware():
    return common.Provider.objects.create(
        name=constants.Provider.VMWARE
    )

# --- common : Company

@pytest.fixture
def mce_app_company():
    return G(common.Company, name="my-company")


# --- account : User

@pytest.fixture
def mce_app_user_with_company(mce_app_company):
    # Token
    return account.User.objects.create(username="user1", email="user2@localhost.net", company=mce_app_company)

@pytest.fixture
def mce_app_user_without_company():
    # Token
    return account.User.objects.create(username="user2", email="user2@localhost.net")


# --- common : ResourceType

@pytest.fixture
def mce_app_resource_type(mce_app_provider):
    return G(common.ResourceType, 
        name="aws.ec2.instance",
        description="EC2 Instance",
        provider=mce_app_provider
    )

@pytest.fixture
def mce_app_resource_type_aws(mce_app_resource_type):
    return mce_app_resource_type

@pytest.fixture
def mce_app_resource_type_azure(mce_app_provider_azure):
    return G(common.ResourceType,
        name="microsoft.classiccompute/virtualmachines",
        description="Azure VirtualMachine",
        provider=mce_app_provider_azure
    )

@pytest.fixture
def mce_app_resource_type_azure_group(mce_app_provider_azure):
    return G(common.ResourceType, 
        name="microsoft.resources/resourcegroups",
        provider=mce_app_provider_azure
    )

@pytest.fixture
def mce_app_resource_type_azure_vm(mce_app_resource_type_azure):
    return mce_app_resource_type_azure

@pytest.fixture
def mce_app_resource_type_vsphere_datacenter(mce_app_provider_vmware):
    return G(common.ResourceType,
        name="vmware/Datacenter",
        description="Vsphere DataCenter",
        provider=mce_app_provider_vmware
    )

@pytest.fixture
def mce_app_resource_type_vsphere_vm(mce_app_provider_vmware):
    return G(common.ResourceType,
        name="vmware/VirtualMachine",
        description="Vsphere VirtualMachine",
        provider=mce_app_provider_vmware
    )


# --- common : Tag

@pytest.fixture
def mce_app_tag():
    return common.Tag.objects.create(
        name="ms-resource-usage",
        value="azure-cloud-shell"
    )

@pytest.fixture
def mce_app_tag_with_provider(mce_app_provider):
    return common.Tag.objects.create(
        name="key1",
        value="value1",
        provider=mce_app_provider
    )


# --- common : GenericAccount

# @pytest.fixture
# def mce_app_generic_account(mce_app_company):
#     return G(common.GenericAccount, company=mce_app_company)


# --- common : Resource

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

# -- Vmware Vsphere

@pytest.fixture
def mce_app_vsphere_vcenter(mce_app_company):
    return vsphere.Vcenter.objects.create(
        name="Vcenter1",
        url="https://labo.net?username=user&password=pass",
        company=mce_app_company
    )

@pytest.fixture
def mce_app_vsphere_datacenter(mce_app_company, mce_app_vsphere_vcenter, mce_app_provider_vmware, mce_app_resource_type_vsphere_datacenter):
    return vsphere.DatacenterVMware.objects.create(
        name="DC0",
        resource_id="group-d1/datacenter-dc0",
        resource_type=mce_app_resource_type_vsphere_datacenter,
        company=mce_app_company,
        vcenter=mce_app_vsphere_vcenter,
        provider=mce_app_provider_vmware
    )

@pytest.fixture
def mce_app_vsphere_resource(mce_app_company, mce_app_vsphere_vcenter, mce_app_provider_vmware, mce_app_resource_type_vsphere_vm, mce_app_vsphere_datacenter):
    return vsphere.ResourceVMware.objects.create(
        name="myvm",
        resource_id="group-d1/datacenter-dc0/folder-1/vm-myvm",
        resource_type=mce_app_resource_type_vsphere_vm,
        company=mce_app_company,
        provider=mce_app_provider_vmware,
        datacenter=mce_app_vsphere_datacenter
    )


# -- AWS

@pytest.fixture
def mce_app_subscription_aws(mce_app_provider_aws, mce_app_company):

    return aws.SubscriptionAWS.objects.create(
        subscription_id=str(uuid4()),
        name="sub1",
        company=mce_app_company,
        provider=mce_app_provider_aws,
        tenant=str(uuid4()),
        location="francecentral",
    )


# -- Azure

@pytest.fixture
def mce_app_subscription_azure(mce_app_provider_azure, mce_app_company):

    return azure.SubscriptionAzure.objects.create(
        subscription_id=str(uuid4()),
        name="sub1",
        company=mce_app_company,
        provider=mce_app_provider_azure,
        tenant=str(uuid4()),
        location="francecentral",
    )

@pytest.fixture
def mce_app_resource_group_azure(mce_app_company, mce_app_subscription_azure, mce_app_resource_type_azure_group):
    """Return 1 Azure Resource Group with ResourceGroup Type"""

    name = "rg1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.subscription_id}/resourceGroups/{name}/providers/{mce_app_resource_type_azure_group.name}/{name}"

    return azure.ResourceAzure.objects.create(
        resource_id=resource_id,
        name=name,
        resource_type=mce_app_resource_type_azure_group,
        company=mce_app_company,
        subscription=mce_app_subscription_azure,
        provider=mce_app_resource_type_azure_group.provider,
        location="francecentral",
    )


@pytest.fixture
def mce_app_resource_azure(
    mce_app_company, 
    mce_app_subscription_azure, 
    mce_app_resource_group_azure, 
    mce_app_resource_type_azure, 
    mce_app_tag):

    name = "vm1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.subscription_id}/resourceGroups/{mce_app_resource_group_azure.name}/providers/{mce_app_resource_type_azure.name}/{name}"

    resource = azure.ResourceAzure.objects.create(
        resource_id=resource_id,
        name=name,
        resource_type=mce_app_resource_type_azure,
        company=mce_app_company,
        resource_group=mce_app_resource_group_azure,
        subscription=mce_app_subscription_azure,
        provider=mce_app_resource_type_azure.provider,
        location="francecentral",
        
    )
    resource.tags.add(mce_app_tag)
    return resource


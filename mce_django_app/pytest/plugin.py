"""
Add to test/conftest.py module:
pytest_plugins = "mce_django_app.pytest.plugin"
"""

from uuid import uuid4
import pytest
from ddf import G, M
from freezegun import freeze_time
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common
from mce_django_app.models import azure
from mce_django_app.models import vsphere
from mce_django_app.models import aws
#from mce_django_app.models import gcp

USER_MODEL = get_user_model()

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

@pytest.fixture
def mce_app_provider_all(
        mce_app_provider_azure,
        mce_app_provider_vmware,
        mce_app_provider_aws,
        mce_app_provider_gcp
    ):
    return [
        mce_app_provider_azure,
        mce_app_provider_vmware,
        mce_app_provider_aws,
        mce_app_provider_gcp
    ]

# --- common: Region

@pytest.fixture
def mce_app_region(mce_app_provider):
    return common.Region.objects.create(
        name="us-east-1",
        display_name="US East 1",
        provider=mce_app_provider
    )

@pytest.fixture
def mce_app_region_aws(mce_app_region):
    return mce_app_region

@pytest.fixture
def mce_app_region_azure(mce_app_provider_azure):
    return common.Region.objects.create(
        name="centralus",
        display_name="Central US",
        provider=mce_app_provider_azure
    )

# --- django.contrib.auth : Group

# @pytest.fixture
# def mce_app_company_group_admins():
#     return Group.objects.create(name="my_company_Admins")
#
# @pytest.fixture
# def mce_app_company_group_users():
#     return Group.objects.create(name="my_company_Users")
#
# @pytest.fixture
# def mce_app_company2_group_admins2():
#     return Group.objects.create(name="my_company2_Admins")
#
# @pytest.fixture
# def mce_app_company2_group_users2():
#     return Group.objects.create(name="my_company2_Users")


# --- common: SyncSettings

@pytest.fixture
def mce_app_syncsettings(mce_app_provider_all, mce_app_region):

    settings = common.SyncSettings.objects.create(
        name="test",
        inventory_mode=constants.InventoryMode.PULL,
        delete_mode=constants.DeleteMode.DISABLE,
        #include_resource_types
    )
    settings.include_providers.set(mce_app_provider_all)
    settings.include_regions.set([mce_app_region])

    return settings


# --- common : Company

@pytest.fixture
def mce_app_company(mce_app_syncsettings):

    return common.Company.objects.create(
        name="my-company",
        settings=mce_app_syncsettings
    )

@pytest.fixture
def mce_app_company2(mce_app_syncsettings):

    return common.Company.objects.create(
        name="my-company2",
        settings=mce_app_syncsettings
    )

# --- account : User

@pytest.fixture
def mce_app_user_with_company(mce_app_company):
    """Admin user for company"""

    return USER_MODEL.objects.create_user(
        username="company_user_1",
        email="company_user_1@localhost.net",
        company=mce_app_company,
        role=constants.UserRole.OWNER,
        password="password",
        is_staff=True
    )


@pytest.fixture
def mce_app_user_admin(mce_app_user_with_company):
    return mce_app_user_with_company


@pytest.fixture
def mce_app_user_user(mce_app_company):
    """Normal user for company"""

    return USER_MODEL.objects.create_user(
        username="company_user_2",
        email="company_user_2@localhost.net",
        company=mce_app_company,
        role=constants.UserRole.USER,
        password="password",
        is_staff=True
    )


@pytest.fixture
def mce_app_user_without_company():

    return USER_MODEL.objects.create_user(
        username="user3",
        email="user3@localhost.net",
        password="password",
        is_staff=True
    )


@pytest.fixture
def mce_app_user_with_other_company(mce_app_company2):
    """Admin user for company"""

    return USER_MODEL.objects.create_user(
        username="user_company2",
        email="user_company2@localhost.net",
        company=mce_app_company2,
        role=constants.UserRole.USER,
        password="password",
        is_staff=True
    )


@pytest.fixture
def mce_app_service_user(mce_app_company):
    """Service user for company"""

    # not create_user() function because no password
    obj = USER_MODEL.objects.create(
        username="company_user_service",
        email="company_user_service@localhost.net",
        company=mce_app_company,
        role=constants.UserRole.SERVICE
    )
    assert not getattr(obj, "auth_token", None) is None
    #obj.groups.add(mce_app_company_group_users)
    return obj

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
def mce_app_tag(mce_app_company, mce_app_provider):
    return common.Tag.objects.create(
        company=mce_app_company,
        provider=mce_app_provider,
        name="key1",
        value="value1"
    )


# --- common : Resource

@pytest.fixture
def mce_app_resource(mce_app_resource_type, mce_app_company):
    """Simple minimal resource without tags and metas"""

    obj = common.Resource.objects.create(
        name="myname",
        resource_id="x1",
        resource_type=mce_app_resource_type,
        company=mce_app_company,
        provider=mce_app_resource_type.provider,
    )
    #obj.tags.set(G(common.Tag, company=mce_app_company, provider=mce_app_resource_type.provider, n=3))
    return obj

# @pytest.fixture
# def mce_app_resource_list(mce_app_resource_type, mce_app_company):
#     """Return 10 Resource instance with 3 tags"""
#
#     return G(common.Resource,
#         resource_type=mce_app_resource_type,
#         provider=mce_app_resource_type.provider,
#         company=mce_app_company,
#         tags=G(common.Tag, provider=mce_app_resource_type.provider, n=3),
#         n=10,
#     )

# -- Vmware Vsphere

@pytest.fixture
def mce_app_vsphere_vcenter(mce_app_company, mce_app_provider_vmware):
    return vsphere.Vcenter.objects.create(
        name="Vcenter1",
        url="https://labo.net?username=user&password=pass",
        company=mce_app_company,
        provider=mce_app_provider_vmware
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
    )

@pytest.fixture
def mce_app_resource_group_azure(
    mce_app_company,
    mce_app_subscription_azure,
    mce_app_resource_type_azure_group,
    mce_app_region_azure):
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
        region=mce_app_region_azure,
    )


@pytest.fixture
def mce_app_resource_azure(
    mce_app_company, 
    mce_app_subscription_azure,
    mce_app_region_azure,
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
        region=mce_app_region_azure,
    )
    resource.tags.add(mce_app_tag)
    return resource


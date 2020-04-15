import pytest
from ddf import G
from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common

"""
Microsoft.Resources/resourceGroups
Microsoft.ClassicCompute/virtualMachines
Microsoft.Sql/servers/databases
"""

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
def mce_app_tags_five():
    return G(common.Tag, n=5)

@pytest.fixture
def mce_app_generic_account():
    return G(common.GenericAccount)




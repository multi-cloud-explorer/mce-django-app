import pytest

from django.db.models.deletion import ProtectedError

from mce_django_app.models import common as models
from mce_django_app.models.azure import SubscriptionAzure, ResourceAzure
from mce_django_app.models.vsphere import Vcenter, DatacenterVMware, ResourceVMware
from mce_django_app.models.account import User

# TODO: move to specific model

@pytest.mark.skip("TODO")
def test_company_on_delete(
        mce_app_company,
        mce_app_generic_account,
        mce_app_user_with_company,
        #mce_app_provider_vmware,
        mce_app_vsphere_datacenter,
        mce_app_subscription_azure,
        mce_app_resource,
        mce_app_resource_azure):
    """test delete propagation for Company"""

    with pytest.raises(ProtectedError) as excinfo:
        mce_app_company.delete()

    # TODO: excinfo.value.protected_objects
    # TODO: excinfo.value.args

    mce_app_resource.delete()
    mce_app_resource_azure.delete()
    #mce_app_resource_group_azure.delete()
    mce_app_subscription_azure.delete()

    # count, object = 
    mce_app_company.delete()

    # CASCADE
    #assert models.GenericAccount.objects.count() == 0

    # PROTECT
    assert models.Resource.objects.count() == 0
    
    # PROTECT
    assert SubscriptionAzure.objects.count() == 0
    
    # PROTECT
    assert ResourceAzure.objects.count() == 0

    # SET NULL
    assert User.objects.count() == 1
    assert User.objects.first().company is None

@pytest.mark.skip("TODO")
def test_resource_azure_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_subscription_azure_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_generic_account_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_user_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_resource_event_change_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_resource_type_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_resource_on_delete():
    """test delete propagation"""

@pytest.mark.skip("TODO")
def test_tag_on_delete():
    """test delete propagation"""

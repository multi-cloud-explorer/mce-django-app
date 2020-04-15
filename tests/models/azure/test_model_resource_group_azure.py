import pytest

from freezegun import freeze_time

from mce_django_app.models.common import ResourceType
from mce_django_app import constants
from mce_django_app.models import azure as models

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@freeze_time("2019-01-01")
def test_resource_group_azure_success(subscription, tags):

    resource_type = ResourceType.objects.create(
        name="Microsoft.Resources/resourceGroups",
        provider=constants.Provider.AZURE
    )
    
    name = "rg1"
    resource_id = f"/subscriptions/{subscription.pk}/resourceGroups/{name}/providers/{resource_type.name}/{name}"
    
    resource = models.ResourceGroupAzure.objects.create(
        id=resource_id,
        name=name,
        resource_type=resource_type,
        subscription=subscription,
        provider=constants.Provider.AZURE,
        location="francecentral",
    )
    resource.tags.set(tags)

    assert resource.active is True
    assert resource.tags.count() == 5
    assert resource.metas == {}
    #assert resource.deleted is False
    assert resource.locked is False

    # TODO: test date freeze
    assert resource.created is not None

    assert resource.updated is None

@pytest.mark.skip("TODO")
def test_resource_group_azure_error_duplicate():
    """check error if resource_group_azure exist"""

@pytest.mark.skip("TODO")
def test_resource_group_azure_error_max_length():
    """Test max_length on name and description"""

@pytest.mark.skip("TODO")
def test_resource_group_azure_error_null_and_blank_value():
    """test null and blank value"""

@pytest.mark.skip("TODO")
def test_resource_group_azure_on_delete():
    """test delete propagation"""

import pytest

from django.core.exceptions import ValidationError
from freezegun import freeze_time

from mce_django_app import constants
from mce_django_app.models import azure as models

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@freeze_time("2019-01-01")
def test_resource_azure_success(
    mce_app_azure_subscription, 
    mce_app_azure_resource_group, 
    mce_app_company,
    mce_app_resource_type_azure_vm, 
    mce_app_tags_five):

    name = "vm1"
    resource_id = f"/subscriptions/{mce_app_azure_subscription.subscription_id}/resourceGroups/{mce_app_azure_resource_group.name}/providers/{mce_app_resource_type_azure_vm.name}/{name}"

    resource = models.ResourceAzure.objects.create(
        resource_id=resource_id,
        name=name,
        company=mce_app_company,
        resource_type=mce_app_resource_type_azure_vm,
        resource_group=mce_app_azure_resource_group,
        subscription=mce_app_azure_subscription,
        provider=constants.Provider.AZURE,
        location="francecentral",
    )

    assert resource.slug == f"subscriptions-{mce_app_azure_subscription.subscription_id}-resourcegroups-rg1-providers-microsoft-classiccompute-virtualmachines-vm1"

    resource.tags.set(mce_app_tags_five)

    assert resource.provider == constants.Provider.AZURE
    assert resource.tags.count() == 5
    assert resource.metas == {}
    #assert resource.deleted is False
    assert resource.locked is False

    # TODO: test date freeze
    assert resource.created is not None

    assert resource.updated is None

def test_resource_azure_error_with_null_or_blank(
    mce_app_azure_subscription, 
    mce_app_azure_resource_group, 
    mce_app_company,
    mce_app_resource_type_azure_vm):
    """test error for null or blank values"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceAzure.objects.create(
            resource_id=None,
            name=None,
            company=None,
            resource_type=None,
            provider=None,
            location=None,
            subscription=None,
            resource_group=None,
            kind=None,
            sku=None,
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be null.'], 
        'name': ['This field cannot be null.'], 
        'company': ['This field cannot be null.'], 
        'resource_type': ['This field cannot be null.'], 
        'provider': ['This field cannot be null.'], 
        'location': ['This field cannot be null.'], 
        'subscription': ['This field cannot be null.'], 
        'resource_group': ['This field cannot be null.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceAzure.objects.create(
            resource_id='',
            name='',
            company=mce_app_company,
            resource_type=mce_app_resource_type_azure_vm,
            provider='',
            location='',
            subscription=mce_app_azure_subscription,
            resource_group=mce_app_azure_resource_group,
            kind='',
            sku={},
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
        'provider': ['This field cannot be blank.'], 
        'location': ['This field cannot be blank.'], 
    }

@pytest.mark.skip("TODO")
def test_resource_azure_on_delete():
    """test delete propagation"""

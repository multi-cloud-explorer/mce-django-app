import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models.common import  ResourceEventChange
from mce_django_app.models import azure as models

CURRENT_MODEL = models.ResourceAzure

def test_resource_azure_success(
        mce_app_subscription_azure,
        mce_app_resource_group_azure,
        mce_app_company,
        mce_app_provider_azure,
        mce_app_region_azure,
        mce_app_resource_type_azure_vm):
    """Simple create"""

    name = "vm1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.subscription_id}/resourceGroups/{mce_app_resource_group_azure.name}/providers/{mce_app_resource_type_azure_vm.name}/{name}"

    resource = CURRENT_MODEL.objects.create(
        resource_id=resource_id,
        name=name,
        company=mce_app_company,
        resource_type=mce_app_resource_type_azure_vm,
        resource_group=mce_app_resource_group_azure,
        subscription=mce_app_subscription_azure,
        provider=mce_app_provider_azure,
        region=mce_app_region_azure,
    )

    assert resource.slug == f"subscriptions-{mce_app_subscription_azure.subscription_id}-resourcegroups-rg1-providers-microsoft-classiccompute-virtualmachines-vm1"

    #assert ResourceEventChange.objects.count() == 2 # Resource Group + Resource
    #events = [event.new_object["name"] for event in ResourceEventChange.objects.all()]
    #assert events == ["rg1", "vm1"]


def test_resource_azure_error_with_null_or_blank(
        mce_app_subscription_azure,
        mce_app_resource_group_azure,
        mce_app_company,
        mce_app_region_azure,
        mce_app_provider_azure,
        mce_app_resource_type_azure_vm):
    """test error for null or blank values"""

    # TODO: test size sur  kind et location

    # RelatedObjectDoesNotExist
    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            resource_id=None,
            name=None,
            company=None,
            resource_type=None, #mce_app_resource_type_azure_vm,
            provider=None,
            region=None,
            subscription=None, #mce_app_subscription_azure,
            resource_group=None,
            kind=None,
            sku=None,
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be null.'],
        'name': ['This field cannot be null.'],
        'company': ['This field cannot be null.'],
        'provider': ['This field cannot be null.'],
        'resource_type': ['This field cannot be null.'],
        'region': ['This field cannot be null.'],
        'subscription': ['This field cannot be null.'],
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            resource_id='',
            name='',
            company=mce_app_company,
            resource_type=mce_app_resource_type_azure_vm,
            provider=mce_app_provider_azure,
            region=mce_app_region_azure,
            subscription=mce_app_subscription_azure,
            resource_group=mce_app_resource_group_azure,
            kind='',
            sku={},
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
    }


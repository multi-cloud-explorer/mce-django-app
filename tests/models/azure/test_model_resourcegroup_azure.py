import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models.common import  ResourceEventChange
from mce_django_app.models import azure as models

CURRENT_MODEL = models.ResourceAzure

def test_resource_group_azure_success(
        mce_app_subscription_azure,
        mce_app_company,
        mce_app_provider_azure,
        mce_app_resource_type_azure_group):
    """Simple create"""

    name = "rg1"
    resource_id = f"/subscriptions/{mce_app_subscription_azure.subscription_id}/resourceGroups/{name}/providers/{mce_app_resource_type_azure_group.name}/{name}"

    resource = CURRENT_MODEL.objects.create(
        resource_id=resource_id,
        name=name,
        company=mce_app_company,
        resource_type=mce_app_resource_type_azure_group,
        subscription=mce_app_subscription_azure,
        provider=mce_app_provider_azure,
        location="francecentral",
    )

    assert resource.slug == f"subscriptions-{mce_app_subscription_azure.subscription_id}-resourcegroups-rg1-providers-microsoft-resources-resourcegroups-rg1"
    assert ResourceEventChange.objects.count() == 1
    events = [event.new_object["name"] for event in ResourceEventChange.objects.all()]
    assert events == ["rg1"]

def test_resource_group_azure_error_with_null_or_blank(
        mce_app_subscription_azure,
        mce_app_company,
        mce_app_provider_azure,
        mce_app_resource_type_azure_group):
    """test error for null or blank values"""

    # TODO: test size sur  kind et location

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            resource_id=None,
            name=None,
            company=None,
            resource_type=mce_app_resource_type_azure_group,
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
        'provider': ['This field cannot be null.'],
        'location': ['This field cannot be null.'],
        'subscription': ['This field cannot be null.'],
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            resource_id='',
            name='',
            company=mce_app_company,
            resource_type=mce_app_resource_type_azure_group,
            provider=mce_app_provider_azure,
            location='',
            subscription=mce_app_subscription_azure,
            kind='',
            sku={},
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
        'location': ['This field cannot be blank.'],
    }


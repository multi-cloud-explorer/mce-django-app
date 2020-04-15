import pytest

from django.core.exceptions import ValidationError
from freezegun import freeze_time

from mce_django_app import constants
from mce_django_app.models import azure as models

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@freeze_time("2019-01-01")
def test_resource_azure_success(subscription, resource_group, resource_type, tags):

    name = "vm1"
    resource_id = f"/subscriptions/{subscription.pk}/resourceGroups/{resource_group.name}/providers/{resource_type.name}/{name}"

    resource = models.ResourceAzure.objects.create(
        id=resource_id,
        name=name,
        resource_type=resource_type,
        resource_group=resource_group,
        subscription=subscription,
        provider=constants.Provider.AZURE,
        location="francecentral",
    )
    resource.tags.set(tags)

    assert resource.provider == constants.Provider.AZURE
    assert resource.tags.count() == 5
    assert resource.metas == {}
    #assert resource.deleted is False
    assert resource.locked is False

    # TODO: test date freeze
    assert resource.created is not None

    assert resource.updated is None

def test_resource_azure_error_with_null_or_blank(subscription, resource_group, resource_type):
    """test error for null or blank values"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceAzure.objects.create(
            id=None,
            name=None,
            resource_type=None,
            provider=None,
            location=None,
            subscription=None,
            resource_group=None,
            kind=None,
            sku=None,
        )
    assert excinfo.value.message_dict == {
        'id': ['This field cannot be null.'], 
        'name': ['This field cannot be null.'], 
        'resource_type': ['This field cannot be null.'], 
        'provider': ['This field cannot be null.'], 
        'location': ['This field cannot be null.'], 
        'subscription': ['This field cannot be null.'], 
        'resource_group': ['This field cannot be null.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceAzure.objects.create(
            id='',
            name='',
            resource_type=resource_type,
            provider='',
            location='',
            subscription=subscription,
            resource_group=resource_group,
            kind='',
            sku={},
        )
    assert excinfo.value.message_dict == {
        'id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
        'provider': ['This field cannot be blank.'], 
        'location': ['This field cannot be blank.'], 
    }

@pytest.mark.skip("TODO")
def test_resource_azure_on_delete():
    """test delete propagation"""

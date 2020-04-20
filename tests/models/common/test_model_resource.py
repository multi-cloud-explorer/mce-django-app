import pytest

from django.core.exceptions import ValidationError
from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app.models import common as models

@freeze_time("2019-01-01")
def test_resource_success(
    mce_app_resource_type, 
    mce_app_company,
    mce_app_tags_five):

    assert models.Resource.objects.count() == 0

    resource = models.Resource.objects.create(
        resource_id="x1",
        name="myname",
        company=mce_app_company,
        resource_type=mce_app_resource_type,
        provider=mce_app_resource_type.provider
    )

    assert resource.slug == "x1"

    resource.tags.set(mce_app_tags_five)

    assert str(resource) == "myname (x1)"

    assert resource.tags.count() == 5
    assert resource.active is True
    assert resource.metas == {}
    #assert resource.deleted is False
    assert resource.locked is False

    # TODO: test date freeze
    assert resource.created is not None

    assert resource.updated is None

    resource.save()

    assert resource.updated is not None

    resource.delete()

    assert models.Resource.objects.count() == 0

    #assert models.Resource.all_objects.count() == 1

def test_resource_error_duplicate(mce_app_resource_type, mce_app_company):

    models.Resource.objects.create(
        resource_id="x1",
        name="myname",
        company=mce_app_company,
        resource_type=mce_app_resource_type,
        provider=mce_app_resource_type.provider
    )

    with pytest.raises(ValidationError) as excinfo:
        models.Resource.objects.create(
            resource_id="x1",
            name="myname",
            company=mce_app_company,
            resource_type=mce_app_resource_type,
            provider=mce_app_resource_type.provider
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['Resource with this Resource id already exists.']
    }

def test_resource_error_null_and_blank_value(mce_app_resource_type, mce_app_company):
    """test error for null or blank values"""

    with pytest.raises(ValidationError) as excinfo:
        models.Resource.objects.create(
            resource_id=None,
            name=None,
            company=None,
            resource_type=None,
            provider=None,
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be null.'], 
        'company': ['This field cannot be null.'], 
        'name': ['This field cannot be null.'], 
        'resource_type': ['This field cannot be null.'], 
        'provider': ['This field cannot be null.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.Resource.objects.create(
            resource_id='',
            name='',
            company=mce_app_company,
            resource_type=mce_app_resource_type,
            provider=''
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
        'provider': ['This field cannot be blank.'], 
    }

def test_resource_error_max_length(mce_app_resource_type, mce_app_company):
    """Test max_length on id and name"""

    with pytest.raises(ValidationError) as excinfo:
        models.Resource.objects.create(
            resource_id="x" * 1025,
            name="x" * 256,
            company=mce_app_company,
            resource_type=mce_app_resource_type,
            provider=mce_app_resource_type.provider
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['Ensure this value has at most 1024 characters (it has 1025).'], 
        'name': ['Ensure this value has at most 255 characters (it has 256).'], 
    }


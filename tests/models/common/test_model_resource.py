import pytest
from pprint import pprint
from datetime import datetime
from dateutil.tz import UTC

from django.core.exceptions import ValidationError
from freezegun import freeze_time

from mce_django_app.models import common as models

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

@freeze_time("2019-01-01")
def test_resource_success(
        mce_app_resource_type_azure,
        mce_app_company):

    assert models.Resource.objects.count() == 0

    resource = models.Resource.objects.create(
        resource_id="x1",
        name="myname",
        company=mce_app_company,
        resource_type=mce_app_resource_type_azure,
        provider=mce_app_resource_type_azure.provider,
        metas={}
    )

    assert resource.slug == "x1"

    assert str(resource) == "azure - microsoft.classiccompute/virtualmachines - myname"

    assert resource.tags.count() == 0
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


@freeze_time("2019-01-01")
def test_resource_to_dict(
        mce_app_resource_type,
        mce_app_company,
        mce_app_tag):

    resource = models.Resource.objects.create(
        resource_id="x1",
        name="myname",
        company=mce_app_company,
        resource_type=mce_app_resource_type,
        provider=mce_app_resource_type.provider,
        metas=dict(key1=1, key2="deux")
    )
    resource.tags.set([mce_app_tag])

    #pprint(resource.to_dict())
    assert resource.to_dict()['metas'] == dict(key1=1, key2="deux")
    assert isinstance(resource.to_dict()['metas'], dict) is True
    assert type(resource.to_dict()['metas']) == dict

    old_obj = resource.to_dict()
    del old_obj['created']

    assert old_obj == {
        'id': 1,
        'resource_id': 'x1',
        'slug': 'x1',
        'name': 'myname',
        'company': 'my-company',
        'provider': "azure",
        'resource_type': 'aws.ec2.instance',
        'tags': [
            {"name": "key1", "value": "value1", "provider": "azure", "company": "my-company"},
        ],
        'metas': {'key1': 1, 'key2': 'deux'},
        'active': True,
        #'categories': [],
        'locked': False,
        # TODO: 'created': datetime(2019, 1, 1, 0, 0, tzinfo=UTC),
        'updated': None
    }
    assert type(old_obj['provider']) == str

    obj, _ = models.Resource.objects.update_or_create(
        resource_id="x1",
        defaults=dict(
            name="myname",
            company=mce_app_company,
            resource_type=mce_app_resource_type,
            provider=mce_app_resource_type.provider,
            metas=dict(key1=2, key2="deux", key3="trois")
        )
    )

    pprint(obj.to_dict())
    assert obj.to_dict()['metas'] == dict(key1=2, key2="deux", key3="trois")
    assert isinstance(obj.to_dict()['metas'], dict) is True
    assert type(obj.to_dict()['metas']) == dict

    assert obj.to_dict() == {
        'id': 1,
        'resource_id': 'x1',
        'slug': 'x1',
        'name': 'myname',
        'company': 'my-company',
        'provider': "azure",
        'resource_type': 'aws.ec2.instance',
        'tags': [
            {"name": "key1", "value": "value1", "provider": "azure", "company": "my-company"},
        ],
        'metas': {'key1': 2, 'key2': 'deux', 'key3': 'trois'},
        'active': True,
        'locked': False,
        'created': datetime(2019, 1, 1, 0, 0, tzinfo=UTC),
        'updated': datetime(2019, 1, 1, 0, 0, tzinfo=UTC)
    }

"""
        data["tags"] = [tag.to_dict(exclude=exclude) for tag in self.tags.all()]

"""



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
            provider=mce_app_resource_type.provider
        )
    assert excinfo.value.message_dict == {
        'resource_id': ['This field cannot be blank.'], 
        'name': ['This field cannot be blank.'], 
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


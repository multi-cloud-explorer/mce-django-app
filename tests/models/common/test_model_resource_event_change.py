import pytest
from django.core.exceptions import ValidationError
import jsonpatch

from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

@pytest.fixture
def resource(resource_type, tags):
    resource = models.Resource.objects.create(
        id="x1",
        name="myname",
        resource_type=resource_type,
        provider=resource_type.provider
    )
    resource.tags.set(tags)
    return resource

def test_resource_event_change_create(resource):
    """CREATE Event for Resource"""

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=resource,
        new_object=resource.to_dict(exclude=['created', 'updated']),
    )

    assert resource.changes.count() == 1

    #qs = models.ResourceEventChange.objects.filter(action=constants.EventChangeType.CREATE)

def test_resource_event_change_update(resource):
    """UPDATE Event for Resource"""

    assert resource.name == "myname"
    
    old_resource = resource
    old_obj = old_resource.to_dict(exclude=["created", "updated"])

    new_resource = models.Resource.objects.get(pk=old_resource.pk)
    new_resource.name = "new-myname"
    new_resource.save()
    new_obj = new_resource.to_dict(exclude=["created", "updated"])
    
    patch = jsonpatch.JsonPatch.from_diff(old_obj, new_obj)

    assert len(list(patch)) == 1

    assert list(patch) == [{
        'op': 'replace', 
        'path': '/name', 
        'value': 'new-myname'
    }]
    
    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.UPDATE,
        content_object=new_resource,
        changes=list(patch),
        old_object=old_obj,
        new_object=new_obj,
        diff=None,
    )

    assert resource.changes.count() == 1

def test_resource_event_change_delete(resource):
    """DELETE Event for Resource"""

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.DELETE,
        content_object=resource,
        old_object=resource.to_dict(exclude=['created', 'updated']),
    )

    assert resource.changes.count() == 1

def test_resource_event_change_create_and_delete(resource):
    """CREATE and DELETE Events for Resource"""

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=resource,
        new_object=resource.to_dict(exclude=['created', 'updated']),
    )

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.DELETE,
        content_object=resource,
        old_object=resource.to_dict(exclude=['created', 'updated']),
    )

    assert resource.changes.count() == 2

@pytest.mark.skip("TODO")
def test_resource_event_change_on_delete():
    """test delete propagation"""

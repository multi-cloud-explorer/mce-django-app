import json
import pytest
from django.core.exceptions import ValidationError
import jsonpatch

from django.core.serializers.json import DjangoJSONEncoder
from freezegun import freeze_time

from mce_django_app import constants
from mce_django_app.models import common as models

def test_resource_event_change_create(mce_app_resource):
    """CREATE Event for Resource"""

    change = models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=mce_app_resource,
        new_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    assert mce_app_resource.changes.count() == 1

    #data = change.to_dict(exclude=["content_object", "object_id", "updated", ])#"content_type"])
    #print(json.dumps(data, cls=DjangoJSONEncoder, indent=4))

    #qs = models.ResourceEventChange.objects.filter(action=constants.EventChangeType.CREATE)

@freeze_time("2019-01-01")
def test_resource_event_change_update(mce_app_resource):
    """UPDATE Event for Resource"""

    old_resource = mce_app_resource
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
    
    change = models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.UPDATE,
        content_object=new_resource,
        changes=list(patch),
        old_object=old_obj,
        new_object=new_obj,
        diff=None,
    )

    assert mce_app_resource.changes.count() == 1

    #data = change.to_dict(exclude=["content_object", "object_id", "updated", ])#"content_type"])
    #print(json.dumps(data, cls=DjangoJSONEncoder, indent=4))

@freeze_time("2019-01-01")
def test_resource_event_change_delete(mce_app_resource):
    """DELETE Event for Resource"""

    change = models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.DELETE,
        content_object=mce_app_resource,
        old_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    assert mce_app_resource.changes.count() == 1

    #data = change.to_dict(exclude=["content_object", "object_id", "updated", ])#"content_type"])
    #print(json.dumps(data, cls=DjangoJSONEncoder, indent=4))

@freeze_time("2019-01-01")
def test_resource_event_change_create_and_delete(mce_app_resource):
    """CREATE and DELETE Events for Resource"""

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=mce_app_resource,
        new_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    models.ResourceEventChange.objects.create(
        action=constants.EventChangeType.DELETE,
        content_object=mce_app_resource,
        old_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    assert mce_app_resource.changes.count() == 2


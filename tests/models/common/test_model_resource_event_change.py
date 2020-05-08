from freezegun import freeze_time

from mce_django_app import constants
from mce_django_app.models import common as models

CURRENT_MODEL = models.ResourceEventChange

def test_resource_event_change_create(mce_app_resource):
    """CREATE Event for Resource"""

    change = CURRENT_MODEL.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=mce_app_resource,
        new_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    assert change.object_id == mce_app_resource.pk

    assert mce_app_resource.changes.count() == 1

    #data = change.to_dict(exclude=["content_object", "object_id", "updated", ])#"content_type"])
    #print(json.dumps(data, cls=DjangoJSONEncoder, indent=4))

    #qs = CURRENT_MODEL.objects.filter(action=constants.EventChangeType.CREATE)

@freeze_time("2019-01-01")
def test_resource_event_change_update(settings, mce_app_resource):
    """UPDATE Event for Resource"""

    settings.MCE_CHANGES_ENABLE = True

    old_resource = mce_app_resource
    old_obj = old_resource.to_dict(exclude=["created", "updated"])

    new_resource = models.Resource.objects.get(pk=old_resource.pk)
    new_resource.name = "new-myname"
    new_resource.save()
    new_obj = new_resource.to_dict(exclude=["created", "updated"])

    change = CURRENT_MODEL.create_event_change_update(old_obj, new_obj, new_resource)

    assert change.changes == [{
        'op': 'replace',
        'path': '/name',
        'value': 'new-myname'
    }]
    assert mce_app_resource.changes.count() == 1

    #data = change.to_dict(exclude=["content_object", "object_id", "updated", ])#"content_type"])
    #print(json.dumps(data, cls=DjangoJSONEncoder, indent=4))

@freeze_time("2019-01-01")
def test_resource_event_change_delete(mce_app_resource):
    """DELETE Event for Resource"""

    change = CURRENT_MODEL.objects.create(
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

    CURRENT_MODEL.objects.create(
        action=constants.EventChangeType.CREATE,
        content_object=mce_app_resource,
        new_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    CURRENT_MODEL.objects.create(
        action=constants.EventChangeType.DELETE,
        content_object=mce_app_resource,
        old_object=mce_app_resource.to_dict(exclude=['created', 'updated']),
    )

    assert mce_app_resource.changes.count() == 2


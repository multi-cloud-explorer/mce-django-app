
from . import constants
from .models.common import  ResourceEventChange

def create_event_change(sender, instance=None, created=None, **kwargs):
    if created:
        ResourceEventChange.objects.create(
            action=constants.EventChangeType.CREATE,
            content_object=instance,
            new_object=instance.to_dict(exclude=['created', 'updated']),
        )

from itertools import chain
import logging

from slugify import slugify

logger = logging.getLogger(__name__)

#__all__ = ['JSONField']

def slugify_resource_id_function(content):
    if content.startswith('/'):
        return slugify(content[1:].replace('/', '-').lower())
    return slugify(content)

def model_instance_to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        # if not getattr(f, 'editable', False):
        #    continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data

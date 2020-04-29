import logging

#from django.utils.text import slugify
from slugify import slugify
from jsonfield import JSONField

logger = logging.getLogger(__name__)

#__all__ = ['JSONField']

def slugify_resource_id_function(content):
    if content.startswith('/'):
        return slugify(content[1:].replace('/', '-').lower())
    return slugify(content)


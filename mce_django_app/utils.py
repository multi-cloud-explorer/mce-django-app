import logging

#from django.utils.text import slugify
from django_extensions.db.fields.json import JSONField as BaseJSONField
from slugify import slugify

logger = logging.getLogger(__name__)

__all__ = ['JSONField']

def slugify_resource_id_function(content):
    if content.startswith('/'):
        return slugify(content[1:].replace('/', '-').lower())
    return slugify(content)

class JSONField(BaseJSONField):
    """Fixe JSONField decode error"""

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        try:
            return super().to_python(value)
        except Exception as err:
            data = (self.name, value, str(err))
            logger.warn("JSONField error - fields[%s] - value[%s] - error[%s]" % data)
            return {}

import logging

from django_extensions.db.fields.json import JSONField as BaseJSONField

logger = logging.getLogger(__name__)

__all__ = ['JSONField']


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

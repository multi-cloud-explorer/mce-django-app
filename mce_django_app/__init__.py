default_app_config = 'mce_django_app.apps.MceAppConfig'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

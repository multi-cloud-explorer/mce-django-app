from django.db import models

import pytest
from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import utils

# TODO: ModelToDictMixin
# TODO: ValidateModelMixin
# TODO: last_error

"""
A mettre dans une app local avec INSTALLED_APPS
class TestJsonModel(models.Model):

    metas = utils.JSONField(
                            default={}, 
                            null=True, blank=True)

"""

@pytest.mark.skip("TODO")
def test_json_field():
    """JSONField Tests"""

    obj = TestJsonModel(metas={"a": "x"})
    assert obj.metas == {"a": "x"}
    obj.full_clean()

    # TODO: invalid JSON


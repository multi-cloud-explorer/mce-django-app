import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

def test_generic_account():
    assert False, "NotImplemented"
    
    # create simple account
    account = models.GenericAccount.objects.create(
        name="test",
        description="TEST",
        username="USER1",
        password="password"
    )

    # TODO: check error if no password or no username
    # TODO: check limit fields length
    # TODO: check unique name

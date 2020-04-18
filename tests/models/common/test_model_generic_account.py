import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

def test_generic_account_success(mce_app_company):
    
    # create simple account
    account = models.GenericAccount.objects.create(
        name="test",
        #description="TEST",
        #username="USER1",
        #password="password",
        company=mce_app_company
    )

@pytest.mark.skip("TODO")
def test_generic_account_error_duplicate():
    """check error if generic_account exist"""

@pytest.mark.skip("TODO")
def test_generic_account_error_max_length():
    """Test max_length on name and description"""

@pytest.mark.skip("TODO")
def test_generic_account_error_null_and_blank_value():
    """test null and blank value"""

@pytest.mark.skip("TODO")
def test_generic_account_on_delete():
    """test delete propagation"""

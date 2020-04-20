import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import common as models

def test_generic_account_success(mce_app_company):
    """simple success create"""
    
    models.GenericAccount.objects.create(
        name="test",
        company=mce_app_company
    )

@pytest.mark.skip("TODO")
def test_generic_account_error_duplicate():
    """check error if duplicate object"""

@pytest.mark.skip("TODO")
def test_generic_account_error_max_length():
    """Test max_length constraints"""

@pytest.mark.skip("TODO")
def test_generic_account_error_null_and_blank_value():
    """test null and blank value"""


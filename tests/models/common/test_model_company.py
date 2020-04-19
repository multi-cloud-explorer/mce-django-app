import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from mce_django_app import constants
from mce_django_app.models import common as models

@pytest.mark.skip("TODO")
def test_company_success():
    """simple success create"""

@pytest.mark.skip("TODO")
def test_company_error_duplicate():
    """check error if duplicate object"""

@pytest.mark.skip("TODO")
def test_company_error_max_length():
    """Test max_length constraints"""

@pytest.mark.skip("TODO")
def test_company_error_null_and_blank_value():
    """test null and blank value"""

@pytest.mark.skip("TODO")
def test_company_on_delete():
    """test delete propagation"""


import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import account as models

def test_user_success(mce_app_company):
    """simple success create"""
    
    models.User.objects.create(
        username="test",
        email="test@localhost.net"
    )

@pytest.mark.skip("TODO")
def test_user_error_duplicate():
    """check error if duplicate object"""

@pytest.mark.skip("TODO")
def test_user_error_max_length():
    """Test max_length constraints"""

@pytest.mark.skip("TODO")
def test_user_error_null_and_blank_value():
    """test null and blank value"""


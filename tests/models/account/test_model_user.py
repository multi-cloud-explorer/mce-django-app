import pytest

from django.core.exceptions import ValidationError
from mce_django_app import constants
from mce_django_app.models import account as models


def test_user_success(mce_app_company):
    """simple success create"""
    
    user = models.User.objects.create(
        username="test",
        role=constants.UserRole.USER,
        email="test@localhost.net",
        company=mce_app_company,
    )
    assert user.is_active is True
    assert user.is_user is True
    assert user.is_superuser is False
    assert user.is_owner is False
    assert user.is_service is False

    assert not user.api_token_key is None
    assert not user.profile is None

    #print("!!! : ", user.to_dict())

@pytest.mark.skip("TODO")
def test_user_error_duplicate():
    """check error if duplicate object"""

@pytest.mark.skip("TODO")
def test_user_error_max_length():
    """Test max_length constraints"""

@pytest.mark.skip("TODO")
def test_user_error_null_and_blank_value():
    """test null and blank value"""


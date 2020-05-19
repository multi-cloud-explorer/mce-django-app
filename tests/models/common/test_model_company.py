import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import common as models

def test_company_success():
    """simple success create"""

    company = models.Company.objects.create(
        name="Company Test",
    )

    assert company.slug == "company-test"


def test_company_error_duplicate():
    """check error if duplicate object"""

    models.Company.objects.create(
        name="Company Test",
    )

    with pytest.raises(ValidationError) as excinfo:
        models.Company.objects.create(
            name="Company Test",
        )        

    assert excinfo.value.message_dict == {
        'name': ['Company with this Name already exists.']
    }

def test_company_error_max_length():
    """Test max_length constraints"""

    with pytest.raises(ValidationError) as excinfo:
        models.Company.objects.create(
            name="x" * 256,
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 256).'], 
    }


def test_company_error_null_and_blank_value():
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        models.Company.objects.create(
            name="",
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.Company.objects.create(
            name=None,
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'], 
    }



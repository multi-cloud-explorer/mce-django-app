import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from mce_django_app import constants
from mce_django_app.models import common as models

def test_tag_without_provider_and_company():
    """create simple tag without provider and company"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
    )

def test_tag_with_provider(mce_app_provider):
    """create simple tag with provider"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
        provider=mce_app_provider
    )

def test_tag_error_if_exist_without_provider():
    """check error if tag without provider exist"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
    )

    with pytest.raises(IntegrityError) as excinfo:
        models.Tag.objects.create(
            name="mytag",
            value="myvalue",
        )

def test_tag_error_if_exist_with_provider(mce_app_provider):
    """check error if tag with provider exist"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
        provider=mce_app_provider
    )

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name="mytag",
            value="myvalue",
            provider=mce_app_provider
        )
    assert excinfo.value.message_dict == {
        '__all__': ['Tag with this Provider, Name and Value already exists.'], 
    }

def test_tag_error_max_length():
    """Test max_length on name and value"""

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name="x" * 257,
            value="x" * 1026,
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 257).'], 
        'value': ['Ensure this value has at most 1024 characters (it has 1026).'], 
    }

def test_tag_error_null_and_blank_value():
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name="",
            value=""
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'], 
        'value': ['This field cannot be blank.']
    }

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name=None,
            value=None,
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'], 
        'value': ['This field cannot be null.'], 
    }


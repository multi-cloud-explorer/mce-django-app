import pytest

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

def test_tag_without_provider():
    """create simple tag without provider"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
    )

def test_tag_without_provider():
    """create simple tag with provider"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
        provider=constants.Provider.AZURE
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

def test_tag_error_if_exist_with_provider():
    """check error if tag with provider exist"""

    models.Tag.objects.create(
        name="mytag",
        value="myvalue",
        provider=constants.Provider.AZURE
    )

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name="mytag",
            value="myvalue",
            provider=constants.Provider.AZURE
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

def test_tag_error_provider_choice():
    """test if provider not in choices"""

    with pytest.raises(ValidationError) as excinfo:
        models.Tag.objects.create(
            name="xxxx",
            value="yxxxx",
            provider="BADCHOICE"
        )
    assert excinfo.value.message_dict == {
        'provider': ["Value 'BADCHOICE' is not a valid choice."]
    }


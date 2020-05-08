import pytest

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from django.core.exceptions import ValidationError

from mce_django_app.models import common as models

CURRENT_MODEL = models.Tag

def test_tag_simple_create(mce_app_company, mce_app_provider):
    """create simple tag"""

    CURRENT_MODEL.objects.create(
        name="mytag",
        value="myvalue",
        provider=mce_app_provider,
        company=mce_app_company
    )

@pytest.mark.mce_known_bug
def test_tag_error_duplicate(mce_app_provider, mce_app_company):
    """check error if tag with provider exist"""

    CURRENT_MODEL.objects.create(
        name="mytag",
        value="myvalue",
        provider=mce_app_provider,
        company=mce_app_company
    )

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="mytag",
            value="myvalue",
            provider=mce_app_provider,
            company=mce_app_company
        )
    assert excinfo.value.message_dict == {
        '__all__': ['Tag with this Company, Provider, Name and Value already exists.'],
    }

def test_tag_error_max_length(mce_app_provider, mce_app_company):
    """Test max_length on name and value"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="x" * 257,
            value="x" * 1026,
            provider=mce_app_provider,
            company=mce_app_company
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 257).'], 
        'value': ['Ensure this value has at most 1024 characters (it has 1026).'], 
    }

def test_tag_error_null_and_blank_value(mce_app_provider, mce_app_company):
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="",
            value="",
            provider=mce_app_provider,
            company=mce_app_company
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'], 
        'value': ['This field cannot be blank.']
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name=None,
            value=None,
        )
    assert excinfo.value.message_dict == {
        'provider': ['This field cannot be null.'],
        'company': ['This field cannot be null.'],
        'name': ['This field cannot be null.'],
        'value': ['This field cannot be null.'], 
    }


import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import common as models

CURRENT_MODEL = models.Region

def test_create_success(mce_app_provider_aws):
    """create simple AWS ResourceType"""

    CURRENT_MODEL.objects.create(
        name="us-east-1",
        display_name="US East 1",
        provider=mce_app_provider_aws
    )


def test_error_duplicate(mce_app_provider_aws):
    """check error if object duplicate"""

    CURRENT_MODEL.objects.create(
        name="us-east-1",
        display_name="US East 1",
        provider=mce_app_provider_aws
    )

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="us-east-1",
            display_name="US East 1",
            provider=mce_app_provider_aws
        )

    assert excinfo.value.message_dict == {
        '__all__': ['Region with this Provider and Name already exists.']
    }

def test_error_max_length(mce_app_provider_aws):
    """Test max_length constraints"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="x" * 256,
            display_name="y" * 256,
            provider=mce_app_provider_aws
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 256).'],
        'display_name': ['Ensure this value has at most 255 characters (it has 256).'],
    }

def test_error_null_and_blank_value(mce_app_provider_aws):
    """test null and blank value constraints"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="",
            display_name="",
            provider=mce_app_provider_aws
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'],
        'display_name': ['This field cannot be blank.'],
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name=None,
            display_name=None,
            provider=None,
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'],
        'display_name': ['This field cannot be null.'],
        'provider': ['This field cannot be null.'],
    }


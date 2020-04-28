import pytest

from django.core.exceptions import ValidationError

from mce_django_app import constants
from mce_django_app.models import common as models

def test_resource_type_success(mce_app_provider_aws):
    """create simple AWS ResourceType"""

    models.ResourceType.objects.create(
        name="aws.ec2.instance",
        description=None,
        provider=mce_app_provider_aws
    )

def test_resource_type_error_duplicate(mce_app_provider_aws):
    """check error if resource_type exist"""

    models.ResourceType.objects.create(
        name="aws.ec2.instance",
        provider=mce_app_provider_aws
    )

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="aws.ec2.instance",
            provider=mce_app_provider_aws
        )        

    assert excinfo.value.message_dict == {
        'name': ['Resource type with this Name already exists.']
    }

def test_resource_type_error_max_length(mce_app_provider_aws):
    """Test max_length on name and description"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="x" * 256,
            description="y" * 256,
            provider=mce_app_provider_aws
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 256).'], 
        'description': ['Ensure this value has at most 255 characters (it has 256).'], 
    }

def test_resource_type_error_null_and_blank_value(mce_app_provider_aws):
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="",
            provider=mce_app_provider_aws
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name=None,
            provider=mce_app_provider_aws
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'], 
    }


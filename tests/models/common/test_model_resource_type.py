import pytest

from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

def test_resource_type_aws():
    """create simple AWS ResourceType"""

    models.ResourceType.objects.create(
        name="aws.ec2.instance",
        description=None,
        provider=constants.Provider.AWS
    )

def test_resource_type_error_if_exist():
    """check error if resource_type exist"""

    models.ResourceType.objects.create(
        name="aws.ec2.instance",
        provider=constants.Provider.AWS
    )

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="aws.ec2.instance",
            provider=constants.Provider.AWS
        )        

    assert excinfo.value.message_dict == {
        'name': ['Resource type with this Name already exists.']
    }

def test_resource_type_error_max_length():
    """Test max_length on name and description"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="x" * 256,
            description="y" * 256,
            provider=constants.Provider.AWS
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 256).'], 
        'description': ['Ensure this value has at most 255 characters (it has 256).'], 
    }

def test_resource_type_error_null_and_blank_value():
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="",
            provider=constants.Provider.AWS
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'], 
    }

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name=None,
            provider=constants.Provider.AWS
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'], 
    }

def test_resource_type_error_provider_choice():
    """test if provider not in choices"""

    with pytest.raises(ValidationError) as excinfo:
        models.ResourceType.objects.create(
            name="xxxx",
            provider="BADCHOICE"
        )
    assert excinfo.value.message_dict == {
        'provider': ["Value 'BADCHOICE' is not a valid choice."]
    }

@pytest.mark.skip("TODO")
def test_resource_type_on_delete():
    """test delete propagation"""

import pytest

from django.core.exceptions import ValidationError

from furl import furl

from mce_django_app import constants
from mce_django_app.models import vsphere as models

CURRENT_MODEL = models.Vcenter

def test_create_success(mce_app_company, mce_app_provider_vmware):
    """Simple create"""

    obj = CURRENT_MODEL.objects.create(
        name="Vcenter1",
        url="https://labo.net?username=user&password=pass",
        company=mce_app_company,
        provider=mce_app_provider_vmware
    )

    assert obj.slug == "vcenter1"

    assert obj.get_auth() == "https://labo.net?username=user&password=pass"

    url = furl(obj.get_auth())
    assert url.host == "labo.net"
    assert url.args.get('username') == "user"
    assert url.args.get('password') == "pass"

def test_error_duplicate(mce_app_company, mce_app_provider_vmware):
    """check error if duplicate object"""

    CURRENT_MODEL.objects.create(
        name="vcenter1",
        url="https://labo.net",
        company=mce_app_company,
        provider=mce_app_provider_vmware
    )

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="vcenter1",
            url="https://labo.net",
            company=mce_app_company,
            provider=mce_app_provider_vmware
        )

    assert excinfo.value.message_dict == {
        'name': ['VMware Vcenter with this Name already exists.'],
        'url': ['VMware Vcenter with this Url already exists.']
    }

def test_error_max_length(mce_app_company, mce_app_provider_vmware):
    """Test max_length constraints"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="x" * 256,
            url="https://%s.net?username=%s" % (("x" * 63), ("x" * 1000)),
            company=mce_app_company,
            provider=mce_app_provider_vmware
        )
    assert excinfo.value.message_dict == {
        'name': ['Ensure this value has at most 255 characters (it has 256).'],
        'url': ['Ensure this value has at most 1024 characters (it has 1085).'],
    }


def test_error_null_and_blank_value(mce_app_company, mce_app_provider_vmware):
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name="",
            url="",
            company=mce_app_company,
            provider=mce_app_provider_vmware
        )

    assert excinfo.value.message_dict == {
        'name': ['This field cannot be blank.'],
        'url': ['This field cannot be blank.'],
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            name=None,
            url=None,
            company=None,
            provider=None
        )
    assert excinfo.value.message_dict == {
        'name': ['This field cannot be null.'],
        'url': ['This field cannot be null.'],
        'company': ['This field cannot be null.'],
        'provider': ['This field cannot be null.'],
    }


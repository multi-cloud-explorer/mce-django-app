from uuid import uuid4

import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import azure as models

CURRENT_MODEL = models.SubscriptionAzure

def test_subscription_azure_success(mce_app_company, mce_app_provider_azure):
    """Simple create"""
    
    subscription_id = str(uuid4())
    subscription_tenant = str(uuid4())

    subscription = CURRENT_MODEL.objects.create(
        subscription_id=subscription_id,
        name="sub1",
        company=mce_app_company,
        provider=mce_app_provider_azure,
        tenant=subscription_tenant,
        username="user",
        password="pass"
        #account=mce_app_generic_account
    )

    assert subscription.is_china is False
    assert subscription.active is True

    auth = subscription.get_auth()

    assert auth == dict(
        subscription_id=subscription_id,
        tenant=subscription_tenant,
        user="user",
        password="pass",
        is_china=False
    )

def test_error_duplicate(mce_app_company, mce_app_provider_azure):
    """check error if duplicate"""

    subscription_id = str(uuid4())
    subscription_tenant = str(uuid4())

    CURRENT_MODEL.objects.create(
        subscription_id=subscription_id,
        name="sub1",
        company=mce_app_company,
        provider=mce_app_provider_azure,
        tenant=subscription_tenant,
    )

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            subscription_id=subscription_id,
            name="sub1",
            company=mce_app_company,
            provider=mce_app_provider_azure,
            tenant=subscription_tenant,
        )
    msg = excinfo.value.message_dict['subscription_id'][0].strip()
    assert msg == 'Azure Subscription with this Subscription id already exists.'

def test_error_max_length(mce_app_company, mce_app_provider_azure):
    """Test max_length on name and description"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            subscription_id="x" * 1025,
            name="x" * 256,
            tenant="x" * 256,
            username="x" * 256,
            password="x" * 256,
            company=mce_app_company,
            provider=mce_app_provider_azure,
        )
    assert excinfo.value.message_dict == {
        'subscription_id': ['Ensure this value has at most 1024 characters (it has 1025).'],
        'name': ['Ensure this value has at most 255 characters (it has 256).'],
        'tenant': ['Ensure this value has at most 255 characters (it has 256).'],
        'username': ['Ensure this value has at most 255 characters (it has 256).'],
        'password': ['Ensure this value has at most 255 characters (it has 256).'],
    }

def test_error_null_and_blank_value(mce_app_company, mce_app_provider_azure):
    """test null and blank value"""

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create(
            subscription_id="",
            name="",
            tenant="",
            company=mce_app_company,
            provider=mce_app_provider_azure,
        )

    assert excinfo.value.message_dict == {
        'subscription_id': ['This field cannot be blank.'],
        'name': ['This field cannot be blank.'],
        'tenant': ['This field cannot be blank.'],
    }

    with pytest.raises(ValidationError) as excinfo:
        CURRENT_MODEL.objects.create()
    assert excinfo.value.message_dict == {
        'subscription_id': ['This field cannot be blank.'],
        'name': ['This field cannot be blank.'],
        'tenant': ['This field cannot be blank.'],
        'company': ['This field cannot be null.'],
        'provider': ['This field cannot be null.'],
    }


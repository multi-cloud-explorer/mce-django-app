from uuid import uuid4

import pytest

from django.core.exceptions import ValidationError

from mce_django_app.models import azure as models

CURRENT_MODEL = models.SubscriptionAzure

def test_subscription_azure_success(mce_app_generic_account, mce_app_company):
    """Create Azure Subscription"""
    
    subscription_id = str(uuid4())
    subscription_tenant = str(uuid4())

    subscription = CURRENT_MODEL.objects.create(
        subscription_id=subscription_id,
        name="sub1",
        company=mce_app_company,
        tenant=subscription_tenant,
        location="francecentral",
        account=mce_app_generic_account
    )

    assert subscription.is_china is False
    assert subscription.active is True

    assert hasattr(mce_app_generic_account, 'mce_django_app_subscriptionazure_related') is True
    
    assert mce_app_generic_account.mce_django_app_subscriptionazure_related.first() == subscription

    auth = subscription.get_auth()

    assert auth == dict(
        subscription_id=subscription_id,
        tenant=subscription_tenant,
        user=mce_app_generic_account.username,
        password=mce_app_generic_account.password,
        is_china=False
    )

@pytest.mark.skip("TODO")
def test_subscription_azure_error_duplicate():
    """check error if subscription exist"""

@pytest.mark.skip("TODO")
def test_subscription_azure_error_max_length():
    """Test max_length on name and description"""

@pytest.mark.skip("TODO")
def test_subscription_azure_error_null_and_blank_value():
    """test null and blank value"""


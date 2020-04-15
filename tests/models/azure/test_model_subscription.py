from uuid import uuid4

import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from freezegun import freeze_time

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app.models.common import GenericAccount
from mce_django_app import constants
from mce_django_app.models import azure as models

def test_subscription_azure(generic_account):
    """Create Azure Subscription"""
    
    subscription_id = uuid4()
    subscription_tenant = uuid4()

    subscription = models.Subscription.objects.create(
        id=subscription_id,
        name="sub1",
        tenant=subscription_tenant,
        location="francecentral",
        account=generic_account
    )

    assert subscription.provider == constants.Provider.AZURE
    assert subscription.is_china is False
    assert subscription.active is True
    
    assert generic_account.subscriptions_azure.first() == subscription

    auth = subscription.get_auth()

    assert auth == dict(
        subscription_id=str(subscription_id),
        tenant=str(subscription_tenant),
        user=generic_account.username,
        password=generic_account.password,
        is_china=False
    )

@pytest.mark.skip("TODO")
def test_subscription_error_duplicate():
    """check error if subscription exist"""

@pytest.mark.skip("TODO")
def test_subscription_error_max_length():
    """Test max_length on name and description"""

@pytest.mark.skip("TODO")
def test_subscription_error_null_and_blank_value():
    """test null and blank value"""

@pytest.mark.skip("TODO")
def test_subscription_on_delete():
    """test delete propagation"""

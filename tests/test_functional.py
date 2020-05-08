from uuid import uuid4
import pytest
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model
from mce_django_app.models import common
from mce_django_app.models import azure

USER_MODEL = get_user_model()

def test_new_company(
    mce_app_provider_azure,
    mce_app_region,
    ):
    """New Company test"""

    # --- Create new Company - 1 par new User
    company = common.Company.objects.create(
        name="Company Test",
    )
    assert not company.owner_group is None
    assert not company.user_group is None

    company.providers.set([mce_app_provider_azure])
    company.regions.set([mce_app_region])

    # --- Create new User
    user = USER_MODEL.objects.create_user(
        "newuser",
        email="newuser@localhost.net",
        password="pass",
        is_staff=True,
        company=company
    )

    # --- Add user to Company Owners group
    user.groups.add(company.owner_group)
    #user.groups.all()
    #company.owner_group.user_set.all()[0].username

    # --- Test permissions checks

    # --- Test api checks

    # # --- OPTIONAL:
    #
    # # --- Add Subscription
    # subscription = azure.SubscriptionAzure.objects.create(
    #     subscription_id=str(uuid4()),
    #     name="new_sub1",
    #     company=company,
    #     provider=mce_app_provider_azure,
    #     tenant=str(uuid4()),
    #     region=mce_app_region,
    # )
    #
    # # --- Test Subscription Connection
    #
    # # --- Schedule Subscription Sync

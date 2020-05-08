import pytest

from ddf import G
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from rest_framework.test import APIRequestFactory, APIClient

@pytest.fixture
def api():
    """Provide an API Request Factory."""
    return APIRequestFactory(enforce_csrf_checks=False)

@pytest.fixture
def client():
    # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return APIClient(enforce_csrf_checks=False)

@pytest.fixture
def user(mce_app_company):
    return G(get_user_model(), company=mce_app_company, password="pass")

@pytest.fixture
def service_user(mce_app_company):
    return G(get_user_model(), company=mce_app_company, is_service=True, password=None)

# @pytest.fixture
# def token(user):
#     token, _ = Token.objects.get_or_create(user=user)
#     return token
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
def api_client():
    # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return APIClient(enforce_csrf_checks=False)


# @pytest.fixture
# def token(user):
#     token, _ = Token.objects.get_or_create(user=user)
#     return token
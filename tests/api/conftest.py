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

@pytest.fixture
def check_perm():
    def _check_perm(client, url, user=None, token=None, status_code=200, count=1):
        if user:
            client.force_authenticate(user=user, token=token)
        response = client.get(url)

        assert response.status_code == status_code

        # pp(response.json())

        if 'count' in response.json():
            assert response.json()['count'] == count
        if 'results' in response.json():
            return response.json()['results']

        return response.json()
    return _check_perm

# @pytest.fixture
# def token(user):
#     token, _ = Token.objects.get_or_create(user=user)
#     return token
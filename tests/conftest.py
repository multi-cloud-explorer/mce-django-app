import pytest

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

pytest_plugins = [
    "mce_django_app.pytest.plugin",
    #"mce_lib_vsphere.pytest.plugin"
]

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture(autouse=True)
def set_default_lang(settings):
    settings.LANGUAGE_CODE = 'en'
    settings.REST_FRAMEWORK['PAGE_SIZE'] = 5

    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }


class MockResponse:
    """
    from unittest.mock import patch

    def test_mytest(mock_response_class):

        with patch("requests.get") as func:
            func.return_value = mock_response_class(200, {"ping": "pong"})
            response = requests.get('http://localhost/ping')
            assert response.status_code == 200
            assert response.json() == {"ping": "pong"}

        with patch("requests.get") as func:
            func.return_value = mock_response_class(500, {}, raise_error=True, reason="server error")
            response = requests.get('http://localhost/ping')
            assert response.status_code == 500
            assert response.json() == {}
    """
    
    def __init__(self, status_code, content, raise_error=None, reason=None):
        self.status_code = status_code
        self.content = content
        self.raise_error = raise_error
        self.reason = reason

    def json(self):
        return self.content

    def raise_for_status(self):
        if self.raise_error:
            raise Exception(self.reason)

    def get_reason(self):
        return self.reason or self.content
         
    text = property(fget=get_reason)

@pytest.fixture(scope="session")
def mock_response_class():
    return MockResponse


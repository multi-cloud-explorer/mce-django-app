import pytest
from ddf import G

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

from mce_django_app import constants
from mce_django_app.models import common as models

@pytest.fixture
def resource_type():
    return models.ResourceType.objects.create(
        name="aws.ec2.instance",
        description=None,
        provider=constants.Provider.AWS
    )

@pytest.fixture
def tags():
    return G(models.Tag, n=5)

@pytest.fixture
def generic_account():
    return G(models.GenericAccount)
from django.db import models

import pytest
from freezegun import freeze_time

from mce_django_app import utils

# TODO: test JSONField

def test_slugify_resource_id_function():

    resource_id = "/subscriptions/1e1c9a88-cc4c-41a0-9176-1af8e593a609/resourceGroups/rg1/providers/Microsoft.ClassicCompute/virtualMachines/vm1"
    
    result = utils.slugify_resource_id_function(resource_id)
    
    assert result == "subscriptions-1e1c9a88-cc4c-41a0-9176-1af8e593a609-resourcegroups-rg1-providers-microsoft-classiccompute-virtualmachines-vm1"

    assert utils.slugify_resource_id_function("x1") == "x1"
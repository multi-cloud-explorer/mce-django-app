"""
    'Provider',
    'Region',
    'Company',
    'ResourceType',
    'Tag',
        company
    'Resource',
        company

    'ResourceEventChange', !!!
        content_object.company

    'SubscriptionAzure',
        company
    'ResourceAzure'
        company

    'Vcenter',
    'DatacenterVMware',
    'ResourceVMware',

"""

DEFAULT_PERMS = [
    dict(scope="model", model="Provider", perms=['view']),
    dict(scope="model", model="Region", perms=['view']),
    #dict(scope="model", model="Zone", perms=['view']),
    dict(scope="model", model="ResourceType", perms=['view']),
    dict(scope="model", model="Company", perms=['view']),
]

ADMINS_PERMS = DEFAULT_PERMS + [
    dict(scope="object", model="Tag", perms=['view', 'change', 'delete']),
    dict(scope="model", model="Tag", perms=['add']),
    dict(scope="object", model="Resource", perms=['view', 'change', 'delete']),
    dict(scope="model", model="Resource", perms=['add']),
    dict(scope="object", model="SubscriptionAzure", perms=['view', 'change', 'delete']),
    dict(scope="model", model="SubscriptionAzure", perms=['add']),
    dict(scope="object", model="ResourceAzure", perms=['view', 'change', 'delete']),
    dict(scope="model", model="ResourceAzure", perms=['add']),
]

USERS_PERMS = DEFAULT_PERMS + [
    dict(scope="object", model="Tag", perms=['view']),
]

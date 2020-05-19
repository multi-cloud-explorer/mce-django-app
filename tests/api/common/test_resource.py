import pytest
from pprint import pprint as pp
from freezegun import freeze_time
from rest_framework.reverse import reverse

from mce_django_app import constants
from mce_django_app.models import common

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

"""
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company
GET_LIST_PERMS_TESTS = [
    dict(company=None, user=dict(is_superuser=True, company=None, role=None), status=200),
    dict(company=dict(name="c1"), user=dict(company="c1", role=constants.UserRole.OWNER), status=200),
]
"""

@pytest.fixture
def resources(api_client, admin_user, mce_app_company, mce_app_company2, mce_app_resource_type):
    url = reverse('common:resource-list')

    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, dict(
        resource_id="company1/x1",
        name="company1/resource1",
        company=mce_app_company.pk,
        resource_type=mce_app_resource_type.pk,
        provider=mce_app_resource_type.provider.pk,
        metas={"key1": "value1"}
    ))
    assert response.status_code == 201
    resource1_id = response.json()['id']

    response = api_client.post(url, dict(
        resource_id="company2/x2",
        name="company2/resource2",
        company=mce_app_company2.pk,
        resource_type=mce_app_resource_type.pk,
        provider=mce_app_resource_type.provider.pk,
        metas={"key1": "value1"}
    ))
    assert response.status_code == 201
    resource2_id = response.json()['id']

    api_client.logout()

    return resource1_id, resource2_id


@freeze_time("2019-01-01")
def test_crud_without_permissions(admin_user, api_client, mce_app_company, mce_app_resource_type,
                                  mce_app_region):

    # --- CREATE with POST
    url = reverse('common:resource-list')
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, dict(
        resource_id="x1",
        name="myname",
        company=mce_app_company.pk,
        resource_type=mce_app_resource_type.pk,
        provider=mce_app_resource_type.provider.pk,
        metas={"key1": "value1"},
        # TODO: tags=[
        #     dict(
        #         company=mce_app_company.pk,
        #         provider=mce_app_resource_type.provider.pk,
        #         name="key",
        #         value="value"
        #     )
        # ]
    ))

    # pp(response.json())
    assert response.status_code == 201

    data = response.json()

    assert data == {
        'id': 1,
        'name': 'myname',
        'resource_id': 'x1',
        'company': 1,
        'provider': 1,
        'resource_type': 1,
        'metas': {"key1": "value1"},
    }


    # --- Retrieve list
    response = api_client.get(url)
    # pp(response.json())
    assert response.status_code == 200

    # assert response.json() == {
    #     'count': 1,
    #     'next': None,
    #     'previous': None,
    #     'results': [
    #         {
    #             'company': 1,
    #             'id': 1,
    #             'metas': {'key1': 'value1'},
    #             'name': 'myname',
    #             'provider': 1,
    #             'resource_id': 'x1',
    #             'resource_type': 1
    #         }
    #     ]
    # }

    data_list = response.json()
    del data_list['results'][0]['created']
    assert data_list == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
         {
            'active': True,
            'company': 'http://testserver/mce/api/v1/common/company/1/',
            #'created': '2019-01-01T00:00:00Z',
            'id': 1,
            'locked': False,
            'metas': {'key1': 'value1'},
            'name': 'myname',
            'provider': 'http://testserver/mce/api/v1/common/provider/1/',
            'resource_id': 'x1',
            'resource_type': 'http://testserver/mce/api/v1/common/resource-type/1/',
            'slug': 'x1',
            'tags': [],
            'updated': None
          }
        ]
     }


    pk = data['id']

    # --- PARTIAL UPDATE with PATCH
    url = reverse('common:resource-detail', args=[pk])
    response = api_client.patch(url, {
        "metas": {"key1": "value2"}
    })
    # pp(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'myname',
        'resource_id': 'x1',
        'company': 1,
        'provider': 1,
        'resource_type': 1,
        'metas': {"key1": "value2"},
    }


    # --- UPDATE REPLACE with PUT
    url = reverse('common:resource-detail', args=[pk])
    response = api_client.put(url, {"name": "my-company-test"})
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method "PUT" not allowed.'}


    # --- DELETE
    url = reverse('common:resource-detail', args=[data['id']])
    response = api_client.delete(url)
    assert response.status_code == 204

    assert common.Resource.objects.count() == 0


def test_permissions_list(
        api_client,
        check_perm,
        resources,
        mce_app_company,
        mce_app_company2,
        mce_app_provider,
        mce_app_region,
        mce_app_resource_type,
        admin_user,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    resource1_id, resource2_id = resources
    assert common.Resource.objects.count() == 2

    url = reverse('common:resource-list')

    # Anonymous user
    check_perm(api_client, url, user=None, status_code=401)

    # Admin user
    results = check_perm(api_client, url, user=mce_app_user_admin, status_code=200, count=1)
    assert results[0]['id'] == resource1_id

    # Normal user
    results = check_perm(api_client, url, user=mce_app_user_user, status_code=200, count=1)
    assert results[0]['id'] == resource1_id

    # Service User
    results = check_perm(
        api_client, url,
        #user=mce_app_service_user,
        token=mce_app_service_user.auth_token,
        status_code=200,
        count=1
    )
    assert results[0]['id'] == resource1_id

    # Admin user for other company
    results = check_perm(api_client, url, user=mce_app_user_with_other_company, status_code=200, count=1)
    assert results[0]['id'] == resource2_id

    # User without company
    response = check_perm(api_client, url, user=mce_app_user_without_company, status_code=403, count=0)
    assert response == {'detail': 'You do not have permission to perform this action.'}

    # Superuser
    results = check_perm(api_client, url, user=admin_user, status_code=200, count=2)
    assert len(results) == 2


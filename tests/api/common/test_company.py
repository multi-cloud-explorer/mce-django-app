import pytest
from pprint import pprint as pp
from freezegun import freeze_time
from rest_framework.reverse import reverse

from mce_django_app import constants
from mce_django_app.models import common

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)

def check_perm(client, url, user=None, token=None, status_code=200, count=1):
    if user:
        client.force_authenticate(user=user, token=token)
    response = client.get(url)

    assert response.status_code == status_code

    #pp(response.json())

    if 'count' in response.json():
        assert response.json()['count'] == count
    if 'results' in response.json():
        return response.json()['results']

    return response.json()


@freeze_time("2019-01-01")
def test_crud_without_permissions(admin_user, api_client):

    # --- CREATE with POST
    url = reverse('common:company-list')
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, {
        "name": "New Company",
    })
    assert response.status_code == 201

    data = response.json()
    #print(data)

    del data['created']
    assert data == {
        'id': 1,
        'inventory_mode': 'pull',
        'name': 'New Company',
        #'owner_group': None,
        #'user_group': None,
        'providers': [],
        'regions': [],
        'resource_types': [],
        'slug': 'new-company',
        #'created': '2020-05-09T14:05:16.753573Z',
        'updated': None,
    }

    pk = data['id']

    # --- PARTIAL UPDATE with PATCH
    url = reverse('common:company-detail', args=[pk])
    response = api_client.patch(url, {"inventory_mode": constants.InventoryMode.PUSH})
    assert response.status_code == 200
    #pp(response.json())

    # --- UPDATE REPLACE with PUT
    url = reverse('common:company-detail', args=[pk])
    response = api_client.put(url, {"name": "my-company-test"})
    assert response.status_code == 200
    #pp(response.json())

    company = common.Company.objects.get(pk=pk)
    provider = common.Provider.objects.create(name=constants.Provider.AZURE)
    tag = common.Tag.objects.create(
        company=company,
        provider=provider,
        name="key",
        value="value"
    )

    # --- DELETE
    url = reverse('common:company-detail', args=[data['id']])
    response = api_client.delete(url)
    assert response.status_code == 204
    # TODO: cascade ????
    #pp(response)

    assert common.Company.objects.count() == 0
    assert common.Tag.objects.count() == 0


def test_permissions_list(
        admin_user,
        api_client,
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    assert common.Company.objects.count() == 2

    url = reverse('common:company-list')

    # Anonymous user
    check_perm(api_client, url, user=None, status_code=401)

    # Admin user
    results = check_perm(api_client, url, user=mce_app_user_admin, status_code=200, count=1)
    assert results[0]['id'] == mce_app_company.pk

    # Normal user
    results = check_perm(api_client, url, user=mce_app_user_user, status_code=200, count=1)
    assert results[0]['id'] == mce_app_company.pk

    # Service User
    results = check_perm(
        api_client, url,
        #user=mce_app_service_user,
        token=mce_app_service_user.auth_token,
        status_code=200,
        count=1
    )
    assert results[0]['id'] == mce_app_company.pk

    # Admin user for other company
    results = check_perm(api_client, url, user=mce_app_user_with_other_company, status_code=200, count=1)
    assert results[0]['id'] == mce_app_company2.pk

    # User without company
    response = check_perm(api_client, url, user=mce_app_user_without_company, status_code=403, count=0)
    assert response == {'detail': 'You do not have permission to perform this action.'}

    # Superuser
    results = check_perm(api_client, url, user=admin_user, status_code=200, count=2)
    assert len(results) == 2


def test_permissions_detail(
        admin_user,
        api_client,
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    url = reverse('common:company-detail', args=[mce_app_company.pk])

    # Anonymous user
    response = check_perm(api_client, url, user=None, status_code=401)
    assert response == {'detail': 'Authentication credentials were not provided.'}

    # Admin user
    response = check_perm(api_client, url, user=mce_app_user_admin, status_code=200, count=1)
    assert response['id'] == mce_app_company.pk

    # Admin user for other company
    response = check_perm(api_client, url, user=mce_app_user_with_other_company, status_code=404, count=0)
    assert response == {'detail': 'Not found.'}

    # User without company
    response = check_perm(api_client, url, user=mce_app_user_without_company, status_code=403, count=0)
    assert response == {'detail': 'You do not have permission to perform this action.'}

    # Admin user for other company
    url = reverse('common:company-detail', args=[mce_app_company2.pk])
    response = check_perm(api_client, url, user=mce_app_user_with_other_company, status_code=200, count=1)
    assert response['id'] == mce_app_company2.pk


def test_permissions_create(
        admin_user,
        api_client,
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    url = reverse('common:company-list')
    response = api_client.post(url, {})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    users = [
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company
    ]
    for user in users:
        api_client.force_authenticate(user=user)
        response = api_client.post(url, {})
        assert response.status_code == 403, user.username

    api_client.force_authenticate(user=admin_user)
    response = api_client.post(url, {
        "name": "new-company"
    })
    assert response.status_code == 201



def test_permissions_update(
        admin_user,
        api_client,
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    url = reverse('common:company-detail', args=[mce_app_company.pk])

    response = api_client.post(url, {})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    # Admin user
    api_client.force_authenticate(user=mce_app_user_admin)
    response = api_client.patch(url, {"inventory_mode": constants.InventoryMode.PUSH})
    assert response.status_code == 200


@pytest.mark.mce_known_bug
def test_permissions_delete(
        admin_user,
        api_client,
        mce_app_company,
        mce_app_company2,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company,
        mce_app_user_without_company):

    assert common.Company.objects.count() == 2

    url_list = reverse('common:company-list')
    response = api_client.delete(url_list)
    assert response.status_code == 401

    url = reverse('common:company-detail', args=[mce_app_company.pk])
    api_client.force_authenticate(user=mce_app_user_admin)
    response = api_client.delete(url)
    assert response.status_code == 403

    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(url) # 405 pour list et 404 sinon
    assert response.status_code == 204
    #print(response.content)
    #pp(response.json())

    # response = api_client.delete(url_list) # 405 pour list et 404 sinon
    # print('!!! : ', response.status_code)
    # print(response.content)

    #assert response.status_code == 200
    """
    {'detail': 'Not found.'}
    {'detail': 'Method "DELETE" not allowed.'}    
    """

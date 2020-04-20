from rest_framework.reverse import reverse

def test_resource_list(client, mce_app_resource_list, mce_app_user_with_company, settings):

    client.force_authenticate(user=mce_app_user_with_company)#, token=token)

    url = reverse('common:resource-list')
    response = client.get(url, format='json')

    assert response.status_code == 200

    #from pprint import pprint as pp
    #pp(response.json())
    assert response.json()['count'] == 10
    assert len(response.json()['results']) == 5

    assert "?limit=5&offset=5" in response.json()['next']

def test_resource_detail(client, mce_app_resource, mce_app_user_with_company):

    client.force_authenticate(user=mce_app_user_with_company)

    url = reverse('common:resource-detail', args=[mce_app_resource.pk])
    response = client.get(url, format='json')

    assert response.status_code == 200

    assert sorted(list(response.json().keys())) == sorted([
        'id',
        'resource_id',
        'slug',
        'resource_type',
        'company',
        'tags',
        'name',
        'provider',
        'metas',
        'locked',
        'active',
        'created',
        'updated',
    ])

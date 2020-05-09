from rest_framework.reverse import reverse

"""
GET common:resource-list
POST common:resource-list
PUT common:resource-detail

mce_app_user_admin
mce_app_user_user
mce_app_user_without_company
"""

# tests permissions
# tests pagination
# tests filters

# def test_resource_list(
#         api_client,
#         mce_app_resource,
#         mce_app_user_admin,
#         mce_app_user_user,
#         mce_app_service_user,
#         mce_app_user_without_company):
#
#     # Anonymous user
#     url = reverse('common:resource-list')
#     response = api_client.get(url, format='json') # follow
#     assert response.status_code == 403
#
#     # Admin user
#
#     # Normal user
#
#     # Service User
#
#     api_client.force_authenticate(user=mce_app_user_admin)
#
#     url = reverse('common:resource-list')
#     response = api_client.get(url, format='json')
#
#     assert response.status_code == 200
#
#     #from pprint import pprint as pp
#     #pp(response.json())
#     assert response.json()['count'] == 1
#     assert len(response.json()['results']) == 1
#
#     assert "?limit=5&offset=5" in response.json()['next']
#
# def test_resource_detail(api_client, mce_app_resource, mce_app_user_with_company):
#
#     api_client.force_authenticate(user=mce_app_user_with_company)
#
#     url = reverse('common:resource-detail', args=[mce_app_resource.pk])
#     response = api_client.get(url, format='json')
#
#     assert response.status_code == 200
#
#     assert sorted(list(response.json().keys())) == sorted([
#         'id',
#         'resource_id',
#         'slug',
#         'resource_type',
#         'company',
#         'tags',
#         'name',
#         'provider',
#         'metas',
#         'locked',
#         'active',
#         'created',
#         'updated',
#     ])

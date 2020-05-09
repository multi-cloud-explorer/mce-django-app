from pprint import pprint as pp
from rest_framework.reverse import reverse

# def test_resource_azure_detail(api_client, mce_app_resource_azure, mce_app_user_with_company):
#
#     api_client.force_authenticate(user=mce_app_user_with_company)#, token=token)
#
#     url = reverse("azure:resourceazure-detail", args=[mce_app_resource_azure.pk])
#
#     response = api_client.get(url, format="json")
#
#     assert response.status_code == 200
#
#     pp(mce_app_resource_azure.to_dict())
#
#     pp(response.json())
#     #pp(sorted(list(response.json().keys())))
#     assert sorted(list(response.json().keys())) == sorted(
#         [
#             "id",
#             "active",
#             "created",
#             "company",
#             "resource_id",
#             "slug",
#             "kind",
#             "region",
#             "locked",
#             "managed_by",
#             "metas",
#             "name",
#             "plan",
#             "provider",
#             "resource_group",
#             "resource_type",
#             "sku",
#             "subscription",
#             "tags",
#             "updated",
#         ]
#     )

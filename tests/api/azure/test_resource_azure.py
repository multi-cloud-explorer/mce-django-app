from rest_framework.reverse import reverse

def test_resource_azure_detail(client, mce_app_azure_resource, mce_app_company_user):

    client.force_authenticate(user=mce_app_company_user)#, token=token)

    url = reverse("azure:resourceazure-detail", args=[mce_app_azure_resource.pk])

    response = client.get(url, format="json")

    assert response.status_code == 200

    from pprint import pprint as pp
    #pp(response.json())
    #pp(sorted(list(response.json().keys())))
    assert sorted(list(response.json().keys())) == sorted(
        [
            "id",
            "active",
            "created",
            "company",
            "resource_id",
            "slug",
            "kind",
            "location",
            "locked",
            "metas",
            "name",
            "provider",
            "resource_group",
            "resource_type",
            "sku",
            "subscription",
            "tags",
            "updated",
        ]
    )

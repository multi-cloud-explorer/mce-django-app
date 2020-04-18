from django.urls import reverse

def test_resource_type_admin_view(
    client, 
    admin_client,
    mce_app_resource_type):

    url = reverse('admin:mce_django_app_resourcetype_changelist') #, args=[mce_app_resource_type.pk])
    response = client.get(url, follow=True)
    
    assert response.status_code == 200

    """
    TODO:
    print(response.context)
    assert 'object_list' in response.context
    
    resource_types = response.context['object_list']
    
    assert resource_types.count() == 1
    
    assert resource_types.first() == mce_app_resource_type
    """
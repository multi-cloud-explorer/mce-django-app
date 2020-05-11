from django.urls import reverse
from pprint import pprint

def test_perms_tag(
        client,
        admin_user,
        mce_app_company,
        mce_app_company2,
        mce_app_tag,
        mce_app_user_admin,
        mce_app_user_user,
        mce_app_service_user,
        mce_app_user_with_other_company):

    url = reverse('admin:mce_django_app_tag_changelist')

    is_logged = client.login(username=admin_user.username, password="password")
    assert is_logged is True
    response = client.get(url, follow=True)
    assert response.status_code == 200
    objects = response.context['cl'].result_list
    assert objects.count() == 1
    assert objects.first().pk == mce_app_tag.pk
    client.logout()

    for user in [mce_app_user_admin, mce_app_user_user]:
        is_logged = client.login(username=user.username, password="password")
        assert is_logged is True
        response = client.get(url, follow=True)
        assert response.status_code == 200
        objects = response.context['cl'].result_list
        assert objects.count() == 1
        assert objects.first().pk == mce_app_tag.pk
        client.logout()

    is_logged = client.login(username=mce_app_user_with_other_company.username, password="password")
    assert is_logged is True
    response = client.get(url, follow=True)
    assert response.status_code == 200
    objects = response.context['cl'].result_list
    assert objects.count() == 0
    client.logout()

    #client.login(username=mce_app_service_user.username, password="password")
    #response = client.get(url, follow=False)
    # TODO: assert response.status_code == 401
    #client.logout()





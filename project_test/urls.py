import re

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.views import serve
from django.urls import re_path
from django.conf import settings

def _serve(request, path, insecure=False, **kwargs):
    return serve(request, path, insecure=True, show_indexes=True, **kwargs)

urlpatterns = [
    #path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('', RedirectView.as_view(pattern_name='admin:index', permanent=True)),
    #path('accounts/', include('allauth.urls')),
    path('adminmce/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('select2/', include('django_select2.urls')),
    #path('mce/app/', include(('mce_django_app.urls', 'mce-django-app'))),
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), _serve),
    path('mce/api/v1/', include('mce_django_app.api.urls')),
]


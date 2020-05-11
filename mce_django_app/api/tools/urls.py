from django.urls import path

from . import metas

urlpatterns = [
    path('metas/', metas.Metas.as_view())
]

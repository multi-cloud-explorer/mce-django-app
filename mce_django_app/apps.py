from django.apps import AppConfig


class MceAppConfig(AppConfig):
    name = 'mce_django_app'
    verbose_name = "Multi Cloud Explorer Application"

    # def ready(self):
    #    print('!!! App ready')
    #    #from django_q.signals import call_hook

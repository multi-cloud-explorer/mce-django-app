from django.core.management.base import BaseCommand

from mce_django_app import constants
from mce_django_app.models.common import Provider

class Command(BaseCommand):
    help = 'Create or Update all providers'

    def _run_command(self):
        _created = 0
        _updated = 0

        for p in constants.Provider:
            provider, created = Provider.objects.update_or_create(name=p.value)
            if created:
                _created += 1
            else:
                _updated += 1

        return _created, _updated

    def handle(self, *args, **options):
        _created, _updated = self._run_command()
        msg = f"create provider - created[{_created}] - updated[{_updated}]"
        self.stdout.write(self.style.SUCCESS(msg))

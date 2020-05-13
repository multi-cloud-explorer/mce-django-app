from django.core.management.base import BaseCommand

from mce_django_app.providers_utils import azure, aws


class Command(BaseCommand):
    help = 'Synchronize Regions for All Providers'

    def _sync_azure(self):
        self.stdout.write(self.style.SUCCESS("start synchronize azure - regions..."))
        result = azure.sync_regions()
        msg = f"synchronized azure - regions - created[{result['created']}] - updated[{result['updated']}]"
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_vsphere(self):
        self.stdout.write(self.style.SUCCESS("no regions for vsphere..."))

    def _sync_aws(self):
        self.stdout.write(self.style.SUCCESS("start synchronize aws - regions..."))
        result = aws.sync_regions()
        msg = f"synchronized aws - regions - created[{result['created']}] - updated[{result['updated']}]"
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_gcp(self):
        raise NotImplementedError()

    def handle(self, *args, **options):
        self._sync_vsphere()
        self._sync_azure()
        self._sync_aws()
        self._sync_gcp()

from django.core.management.base import BaseCommand

from mce_django_app.providers_utils import azure
from mce_django_app.providers_utils import aws
from mce_django_app.providers_utils import vsphere

class Command(BaseCommand):
    help = 'Synchronize Resources Types for All Providers'

    def _sync_azure(self):
        self.stdout.write(self.style.SUCCESS("start synchronize azure..."))
        result = azure.sync_resource_type()
        msg = f"synchronized azure - resources-types - created[{result['created']}] - updated[{result['updated']}]"
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_vsphere(self):
        self.stdout.write(self.style.SUCCESS("start synchronize vsphere..."))
        result = vsphere.sync_resource_type()
        msg = f"synchronized vsphere - resources-types - created[{result['created']}] - updated[{result['updated']}]"
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_aws(self):
        self.stdout.write(self.style.SUCCESS("start synchronize aws..."))
        result = aws.sync_resource_type()
        msg = f"synchronized aws - resources-types - created[{result['created']}] - updated[{result['updated']}]"
        self.stdout.write(self.style.SUCCESS(msg))

    def _sync_gcp(self):
        raise NotImplementedError()

    def handle(self, *args, **options):
        self._sync_azure()
        self._sync_vsphere()
        self._sync_aws()
        self._sync_gcp()


from django.core.management.base import BaseCommand

from tabulate import tabulate
from mce_django_app.models import  common

"""
    'Provider',
    'Company',
    'Tag',
    'ResourceType',
    'Resource',

"""
OBJECTS_LISTS = {
    "company": [common.Company, ["Name"], ["name"]],
    "provider": [common.Provider, ["Name", "Description"], ["name", "description"]],
    "resource_type": [common.ResourceType, ["Name", "Provider"], ["name", "provider.name"]],
    #"subscription": [common.Sub, ["Name", "Description", "Sync"], ["name", "description", "exclude_sync"]],
}

class Command(BaseCommand):

    help = 'Display Objects List'

    def add_arguments(self, parser):

        parser.add_argument(
            '-t', '--type-list',
            dest='type_list',
            choices=list(OBJECTS_LISTS.keys()),
            help='Object to display'
        )

    def handle(self, *args, type_list=None, **options):
        model = OBJECTS_LISTS[type_list][0]
        headers = OBJECTS_LISTS[type_list][1]
        fields = OBJECTS_LISTS[type_list][2]

        data = []

        for o in model.objects.all():
            _data = [getattr(o, f) for f in fields]
            data.append(_data)

        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

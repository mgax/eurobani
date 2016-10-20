from pathlib import Path
from django.core.management.base import BaseCommand
from ... import ingest

class Command(BaseCommand):

    help = "Ingest a table of data"

    def add_arguments(self, parser):
        parser.add_argument('table')
        parser.add_argument('path')

    def handle(self, table, path, **options):
        if table == 'contracts':
            ingest.contracts(Path(path))
        elif table == 'payments':
            ingest.payments(Path(path))
        else:
            print("Unknown table", table)

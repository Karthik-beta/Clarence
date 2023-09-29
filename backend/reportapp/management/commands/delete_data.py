# your_app/management/commands/delete_duplicates.py

from django.core.management.base import BaseCommand
from reportapp.models import ProcessedGislogs

class Command(BaseCommand):
    help = 'Delete duplicate rows from ProcessedGislogs table'

    def handle(self, *args, **options):
        delete_query = '''
        DELETE FROM public.reportapp_processedgislogs
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM public.reportapp_processedgislogs
            GROUP BY employeeid, direction, shortname, serialno, logdate, first_logtime, last_logtime
        );
        '''
        ProcessedGislogs.objects.raw(delete_query)

        self.stdout.write(self.style.SUCCESS('Duplicate rows deleted.'))

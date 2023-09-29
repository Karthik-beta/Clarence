# your_app/management/commands/process_gislogs.py

from django.core.management.base import BaseCommand
from reportapp.models import Gislogs, ProcessedGislogs

from datetime import datetime, timedelta
from itertools import groupby

class Command(BaseCommand):
    help = 'Process and store Gislogs data in ProcessedGislogs table'

    def handle(self, *args, **options):
        # Fetch all data from the Gislogs table ordered by employeeid and logdate
        gislogs_data = Gislogs.objects.all().order_by('employeeid', 'logdate', 'logtime')

        # Define a function to check if first_logtime is equal to last_logtime
        def is_first_logtime_equal_to_last_logtime(group):
            first_logtime = group[0].logtime
            last_logtime = group[-1].logtime
            return first_logtime == last_logtime

        # Group data by employeeid and logdate using itertools.groupby
        grouped_data = groupby(gislogs_data, key=lambda x: (x.employeeid, x.logdate))

        # Calculate total_time for each group and create ProcessedGislogs objects
        processed_data = []
        for (employeeid, logdate), group in grouped_data:
            group = list(group)
            first_logtime = group[0].logtime
            last_logtime = group[-1].logtime

            # Calculate the total_time for the group
            total_time = datetime.combine(logdate, last_logtime) - datetime.combine(logdate, first_logtime)

            # Create a new ProcessedGislogs object and add it to the processed_data list
            processed_data.append(ProcessedGislogs(
                employeeid=employeeid,
                direction=group[0].direction,
                shortname=group[0].shortname,
                serialno=group[0].serialno,
                logdate=logdate,
                first_logtime=first_logtime,
                last_logtime=last_logtime,
                total_time=total_time,
            ))

        # Save the results to the ProcessedGislogs table
        ProcessedGislogs.objects.bulk_create(processed_data)

        self.stdout.write(self.style.SUCCESS('Data processing and storage complete.'))

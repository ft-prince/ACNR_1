import csv
import openpyxl
from django.core.management.base import BaseCommand
from screen_app.models import Unit

class Command(BaseCommand):
    help = 'Import units from Excel or CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the Excel or CSV file')

    def handle(self, *args, **options):
        file_path = options['file']
        units = []

        if file_path.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                code, model = row[:2]
                if code and model:
                    units.append(Unit(code=str(code).strip(), model=str(model).strip()))
        elif file_path.endswith('.csv'):
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 2:
                        code, model = row[:2]
                        if code and model:
                            units.append(Unit(code=str(code).strip(), model=str(model).strip()))
        else:
            self.stdout.write(self.style.ERROR(f'Unsupported file format. Please use .xlsx or .csv'))
            return

        Unit.objects.bulk_create(units, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(units)} units'))

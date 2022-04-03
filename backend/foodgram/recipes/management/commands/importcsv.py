import csv
import time

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Импорт данных в БД
    manage.py importcsv path/to/file.csv main_model m2m_model
    """

    help = 'Imports data from csv-file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Define path to csv file')
        parser.add_argument('model', type=str, help='Define model')

    def handle(self, *args, **options):
        file_path = options["file_path"]
        model_cl = apps.get_model('recipes', model_name=options["model"])
        t1 = time.time()

        with open(file_path, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in reader:
                obj_dict = {key: value for key, value in zip(header, row)}
                model_cl.objects.create(**obj_dict)

        t2 = time.time()

        self.stdout.write(
            self.style.SUCCESS(
                f'File successfully imported! The execution time was: {t2-t1}s!'
            )
        )

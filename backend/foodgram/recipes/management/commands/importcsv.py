import csv
import time

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Импорт данных в БД
    manage.py importcsv path/to/file.csv model_name
    """

    help = 'Imports data from csv-file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Define path to csv file'
        )
        parser.add_argument(
            'model',
            type=str,
            help='Define model name'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        model_cl = apps.get_model('recipes', model_name=options["model"])
        t1 = time.time()

        with open(file_path, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            instances = []
            for row in reader:
                obj_dict = {key: value for key, value in zip(header, row)}
                instances.append(model_cl(**obj_dict))

            model_cl.objects.bulk_create(instances)

        t2 = time.time()

        self.stdout.write(
            self.style.SUCCESS(
                f'File successfully imported!'
                f'The execution time was: {t2-t1}s!'
            )
        )

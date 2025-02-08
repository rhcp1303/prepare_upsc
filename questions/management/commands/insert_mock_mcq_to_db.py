from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from ...helpers import insert_mock_mcq_to_db_helper as helper


class Command(BaseCommand):
    help = 'Load generated mock questions from a JSON file and insert into database'

    def add_arguments(self, parser):
        parser.add_argument('--json_file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        try:
            with open(json_file_path, 'r') as f:
                json_data = f.read()
            helper.load_questions_into_db_from_json(json_data)
            self.stdout.write(self.style.SUCCESS('Questions loaded successfully.'))
        except ValidationError as e:
            self.stderr.write(self.style.ERROR(f'Error loading questions: {e}'))

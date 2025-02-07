from django.core.management.base import BaseCommand
from ...helpers import (extract_questions_helper as helper,
                        common_utils as cu)


class Command(BaseCommand):
    help = 'Extract generated mock mcqs from a text file and write to a JSON file for further use'

    def add_arguments(self, parser):
        parser.add_argument('text_file_path', type=str, help='path to the question paper text')
        parser.add_argument('--pattern_type', type=str, help='type of pattern of questions',
                            choices=[pattern_type.value for pattern_type in cu.PatternType], required=True, )

    def handle(self, *args, **options):
        text_file_path = options['text_file_path']
        with open(text_file_path, "r") as file:
            text = file.read()
        question_dict = helper.extract_mock_questions_from_text(text)
        data = helper.create_mock_mcq_dict(question_dict, cu.PatternType)
        cu.write_to_json(data, 'questions/data/upsc_questions/temp_question_data.json')

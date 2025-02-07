from django.core.management.base import BaseCommand
from ...helpers import (extract_questions_helper as helper,
                        common_utils)


class Command(BaseCommand):
    help = 'Extract previous year questions from a text file and write to a JSON file for further use'

    def add_arguments(self, parser):
        parser.add_argument('text_file_path', type=str, help='path to the question paper text')
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        text_file_path = options['text_file_path']
        year = options['year']
        with open(text_file_path, "r") as file:
            text = file.read()
        question_dict = helper.extract_pyqs_from_text(text)
        data = helper.create_pyq_dict(question_dict, year)
        common_utils.write_to_json(data, 'questions/data/upsc_questions/temp_question_data.json')

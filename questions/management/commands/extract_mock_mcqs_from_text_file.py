from django.core.management.base import BaseCommand
from ...helpers import (extract_questions_helper as helper,
                        common_utils as cu)


class Command(BaseCommand):
    help = 'Extract generated mock mcqs from a text file and write to a JSON file for further use'

    def add_arguments(self, parser):
        parser.add_argument('--text_file_path', type=str, help='path to the question paper text')
        parser.add_argument('--pattern_type', type=str, help='type of pattern of questions',
                            choices=[pattern_type.value for pattern_type in cu.PatternType], required=True, )
        parser.add_argument('--subject', type=str, help='subject of questions',
                            choices=[code.value for code in cu.SubjectCode], required=True, )
        parser.add_argument('--content_type', type=str, help='type of content of questions',
                            choices=[content_type.value for content_type in cu.QuestionContentType], required=True, )

    def handle(self, *args, **options):
        text_file_path = options['text_file_path']
        pattern_type = options['pattern_type']
        subject = options['subject']
        content_type = options['content_type']
        with open(text_file_path, "r") as file:
            text = file.read()
        question_dict = helper.extract_mock_questions_from_text(text)
        data = helper.create_mock_mcq_dict(question_dict, pattern_type, subject, content_type)
        cu.write_to_json(data, text_file_path.replace('.txt', '.json'))

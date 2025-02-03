from django.core.management.base import BaseCommand
from ...helpers import refine_generated_mcq_helper as helper


class Command(BaseCommand):
    help = 'Refine generated mcq by prompting llm'

    def add_arguments(self, parser):
        parser.add_argument('--text_file_path', type=str, help='path to the text file containing generated mcq',
                            required=True)

    def handle(self, *args, **options):
        text_file_path = options['text_file_path']
        helper.refine_generated_mcq(text_file_path)

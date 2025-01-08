from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Use nb classifier model to classify questions into subjects'

    def add_arguments(self, parser):
        parser.add_argument('question_text', type=str, help='question text to be classified into a subject')

    def handle(self, *args, **options):
        from ... helpers import classify_question_into_subjects_helper as helper
        question_text = options['question_text']
        print(helper.classify_text(question_text))

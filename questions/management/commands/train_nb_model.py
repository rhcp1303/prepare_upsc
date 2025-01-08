from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Train nb classifier model to classify questions into subjects'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='path to the training dataset in json format')

    def handle(self, *args, **options):
        from ... helpers import train_nb_model_helper as helper
        json_file_path = options['json_file_path']
        helper.train_nb_multinomial_model_for_text_classification(json_file_path)

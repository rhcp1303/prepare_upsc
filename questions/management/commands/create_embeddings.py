from django.core.management.base import BaseCommand
from ...helpers import embeddings_helper as helper


class Command(BaseCommand):
    help = 'Create embeddings for a pdf to be reused in langchain'

    def add_arguments(self, parser):
        parser.add_argument('pdf_file_path', type=str, help='path to the pdf question paper')

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        embeddings_store_path = pdf_file_path.replace('.pdf','.faiss')
        helper.create_embeddings_and_store(pdf_file_path, embeddings_store_path)

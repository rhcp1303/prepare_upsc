from django.core.management.base import BaseCommand
from ...helpers import embeddings_helper as helper


class Command(BaseCommand):
    help = 'Create embeddings for a pdf to be reused in langchain'

    def add_arguments(self, parser):
        parser.add_argument('--pdf_file_path', type=str, help='path to the pdf question paper', required=True)
        parser.add_argument('--pdf_file_type', type=str, help='type of pdf',
                            choices=['scanned', 'digital'], required=True, )
        parser.add_argument('--number_of_columns', type=int, help='number of columns in the pdf layout', required=True)
        parser.add_argument('--use_llm', type=bool, help='use llm or ocr for extraction', required=True)

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        embeddings_store_path = pdf_file_path.replace('.pdf', '.faiss')
        helper.create_embeddings_and_store(pdf_file_path, embeddings_store_path, pdf_type=options['pdf_type'],
                                           number_of_columns=options['number_of_columns'], use_llm=options['use_llm'])

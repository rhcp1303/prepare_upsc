from django.core.management.base import BaseCommand
from ...helpers import embeddings_helper as helper, common_utils as cu, extract_text_helper as eth


class Command(BaseCommand):
    help = 'Create embeddings (faiss folders) for a pdf file for use in langchain retrieval'

    def add_arguments(self, parser):
        parser.add_argument('--pdf_file_path', type=str, help='path to the pdf question paper', required=True)
        parser.add_argument('--pdf_file_type', type=str, help='type of pdf',
                            choices=[file_type.value for file_type in cu.PDFFileType], required=True, )
        parser.add_argument('--number_of_columns', type=int, help='number of columns in the pdf layout', required=True)
        parser.add_argument('--use_llm', type=str, help='use llm or ocr for extraction', choices=['yes', 'no'],
                            required=True)
        parser.add_argument('--chunk_size', type=int, help='size of the chunk to be created by text splitter',
                            required=True)
        parser.add_argument('--chunk_overlap', type=int, help='overlap of the chunk to be created by text splitter',
                            required=True)

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        pdf_file_type = options['pdf_file_type']
        number_of_columns = options['number_of_columns']
        use_llm = options['use_llm']
        chunk_size = options['chunk_size']
        chunk_overlap = options['chunk_overlap']
        pdf_extractor = eth.select_pdf_extractor(pdf_file_type, number_of_columns, use_llm)
        extracted_text = pdf_extractor.extract_text(pdf_file_path)
        embeddings_store_path = pdf_file_path.replace('.pdf', '.faiss')
        print(extracted_text + "\n\n")
        print(len(extracted_text))
        helper.create_embeddings_and_store(extracted_text, chunk_size, chunk_overlap, embeddings_store_path)

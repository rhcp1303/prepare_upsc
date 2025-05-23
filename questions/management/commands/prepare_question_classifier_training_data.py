from django.core.management.base import BaseCommand
from ...helpers import extract_questions_helper, extract_text_helper, common_utils as cu


class Command(BaseCommand):
    help = 'Prepare JSON file for training question classifier model'

    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, help='subject of the question paper',
                            choices=[code.value for code in cu.SubjectCode], required=False)
        parser.add_argument('--pdf_file_path', type=str, help='path to the pdf question paper', required=True)
        parser.add_argument('--pdf_file_type', type=str, help='type of pdf',
                            choices=[file_type.value for file_type in cu.PDFFileType], required=True, )
        parser.add_argument('--number_of_columns', type=int, help='number of columns in the pdf layout', required=True)
        parser.add_argument('--use_llm', type=str, help='use llm or ocr for extraction', choices=['yes', 'no'],
                            required=True)

    def handle(self, *args, **options):
        subject = options['subject'] or ""
        pdf_file_path = options['pdf_file_path']
        pdf_file_type = options['pdf_file_type']
        number_of_columns = options['number_of_columns']
        use_llm = options['use_llm']
        pdf_extractor = extract_text_helper.select_pdf_extractor(pdf_file_type, number_of_columns, use_llm)
        extracted_text = pdf_extractor.extract_text(pdf_file_path)
        question_dict = extract_questions_helper.extract_questions_from_text(extracted_text)
        question_list = question_dict["list_of_question"]
        data = []
        q = len(question_list)
        for i in range(q):
            data.append({
                "question_text": question_list[i],
                "subject": subject,
            })
        cu.write_to_json(data, 'questions/data/training_data/temp_question_data.json')

from django.core.management.base import BaseCommand
from ...helpers import (load_questions_from_pdf_helper as helper,
                        common_utils as cu)
from ...helpers import pdf_utils as pu


class Command(BaseCommand):
    help = 'Prepare json file for training question classifier model'

    def add_arguments(self, parser):
        parser.add_argument('--pdf_file_path', type=str, help='path to the pdf question paper', required=True)
        parser.add_argument('--pdf_file_type', type=str, help='digital or scanned',
                            choices=[code.value for code in cu.PDFFileType],
                            required=True)
        parser.add_argument('--subject', type=str, help='subject of the question paper',
                            choices=[code.value for code in cu.SubjectCode], required=False)

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        pdf_type = options['pdf_file_type']
        subject = options['subject'] or ""
        if pdf_type == 'scanned':
            extracted_text = pu.TwoColumnScannedPDFExtractorUsingOCR().extract_text(pdf_file_path)
        else:
            extracted_text = pu.TwoColumnDigitalPDFExtractor().extract_text(pdf_file_path)
        with open("temp/training_data.txt", "w") as file:
            file.write(extracted_text)
        question_dict = helper.extract_questions_from_text(extracted_text, "no")
        question_list = question_dict["list_of_question"]
        data = []
        q = len(question_list)
        for i in range(q):
            data.append({
                "question_text": question_list[i],
                "subject": subject,
            })
        cu.write_to_json(data, 'questions/data/training_data/temp_question_data.json')

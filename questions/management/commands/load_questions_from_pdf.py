import time
from django.core.management.base import BaseCommand
import google.generativeai as genai
from ...helpers import common_utils as cu

from ...helpers import (load_questions_from_pdf_helper as question_loader,
                        question_classifier_helper as classifier,
                        common_utils)

model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI")


class Command(BaseCommand):
    help = 'Extract questions from a pdf and ingest to database'

    def add_arguments(self, parser):
        parser.add_argument('pdf_file_path', type=str, help='path to the pdf question paper')
        parser.add_argument('pdf_file_type', type=str, help='pdf file type: digital or scanned',
                            choices=[file_type.value for file_type in cu.PDFFileType])
        parser.add_argument('year', type=int, required=False)

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        pdf_type = options['pdf_file_type']
        year = options['year']
        question_dict = question_loader.load_questions_from_pdf(pdf_file_path, pdf_type)
        data = []
        question_list = question_dict["list_of_question"]
        option_a_list = question_dict["list_of_option_a"]
        option_b_list = question_dict["list_of_option_b"]
        option_c_list = question_dict["list_of_option_c"]
        option_d_list = question_dict["list_of_option_d"]
        print("number of questions extracted: " + str(len(question_list)))
        for i in range(len(question_list)):
            subject = classifier.classify_question(question_list[i])
            explanation = model.generate_content(question_list[i]).text
            time.sleep(5)
            data.append({
                "Q.No.": i + 1,
                "question_text": question_list[i],
                "option_a": option_a_list[i],
                "option_b": option_b_list[i],
                "option_c": option_c_list[i],
                "option_d": option_d_list[i],
                "subject": subject,
                "year": year,
                "explanation": explanation
            })
        common_utils.write_to_json(data,
                                   'upsc_prelims_through_pyq/questions/data/upsc_questions/temp_question_data.json')

import time
from django.core.management.base import BaseCommand
import google.generativeai as genai
from ...helpers import (load_questions_from_pdf_helper as helper,
                        question_classifier_helper as classifier,
                        common_utils as cu, pdf_utils as pu)

model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI")


class Command(BaseCommand):
    help = 'Extract questions from a pdf and write to a JSON file for further use'

    def add_arguments(self, parser):
        parser.add_argument('pdf_file_path', type=str, help='path to the pdf question paper')
        parser.add_argument('pdf_file_type', type=str, help='pdf file type: digital or scanned',
                            choices=[file_type.value for file_type in cu.PDFFileType])
        parser.add_argument('year', type=int, required=False)

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        pdf_type = options['pdf_file_type']
        year = options['year']
        if pdf_type == 'scanned':
            extracted_text = pu.TwoColumnScannedPDFExtractorUsingOCR().extract_text(pdf_file_path)
        else:
            extracted_text = pu.TwoColumnDigitalPDFExtractor().extract_text(pdf_file_path)
        with open("temp/training_data.txt", "w") as file:
            file.write(extracted_text)
        question_dict = helper.extract_questions_from_text(extracted_text, "yes")
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
        cu.write_to_json(data, 'upsc_prelims_through_pyq/questions/data/upsc_questions/temp_question_data.json')

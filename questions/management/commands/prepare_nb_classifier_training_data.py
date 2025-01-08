from django.core.management.base import BaseCommand
from ...helpers import (load_questions_from_pdf_helper as question_loader,
                        common_utils)

class Command(BaseCommand):
    help = 'Prepare csv file for training question classifier model'

    def add_arguments(self, parser):
        parser.add_argument('pdf_file_path', type=str, help='path to the pdf question paper')
        parser.add_argument('pdf_type', type=str, help='digital or scanned', choices=['digital', 'scanned'])
        parser.add_argument('subject', type=str, help='subject of the question paper')

    def handle(self, *args, **options):
        pdf_file_path = options['pdf_file_path']
        pdf_type = options['pdf_type']
        subject = options['subject']
        question_dict = question_loader.load_questions_from_pdf(pdf_file_path, pdf_type,"no")
        question_list = question_dict["list_of_question"]
        data = []
        q = len(question_list)
        for i in range(q):
            data.append({
                "question_text": question_list[i],
                "subject": subject,
            })
        common_utils.write_to_json(data,'questions/data/training_data/temp_question_data.json')
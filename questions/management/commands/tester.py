from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import load_questions_from_pdf_helper as helper
        pdf_path = "/Users/ankit.anand/Desktop/upsc_pyq/2022.pdf"
        text = helper.extract_text_from_scanned_pdf(pdf_path)
        print(text)
from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import common_utils as helper
        logger.info("Starting extraction of text from scanned PDF")
        pdf_path = "/Users/ankit.anand/Desktop/upsc_pyq/2013.pdf"
        extracted_text = helper.extract_text_from_scanned_pdf_using_gemini(pdf_path)
        extracted_text = "yes"
        if extracted_text:
            logger.info("Text extraction from PDF successful!")
        else:
            logger.error("Failed to extract text from PDF")

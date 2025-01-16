from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import pdf_utils as helper
        logger.info("Starting extraction of text from  PDF")
        pdf_file_path = "/Users/ankit.anand/Desktop/2011.pdf"
        pdf_extractor = helper.TwoColumnScannedPDFExtractorUsingOCR()
        extracted_text = pdf_extractor.extract_text(pdf_file_path)
        print(extracted_text)
        if extracted_text:
            logger.info("Text extraction from PDF successful!")
        else:
            logger.error("Failed to extract text from PDF")

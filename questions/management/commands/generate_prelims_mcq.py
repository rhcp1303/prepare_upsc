from django.core.management.base import BaseCommand
from ...helpers import generate_prelims_mcq_from_questions_helper as helper
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info(f"Starting generation of of questions:")
        helper.generate_mock_mcq()

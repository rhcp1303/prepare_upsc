from django.core.management.base import BaseCommand
import logging
from ...helpers import query_question_helper as helper
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This is a utility management command for testing purpose'

    def handle(self, *args, **options):
        helper.query_question()
        print("here")

from django.core.management.base import BaseCommand
import json
from ...helpers import format_helper
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This is a utility management command for formatting flt json for ui presentation'

    def handle(self, *args, **options):
        with open("questions/data/flt/test1.json", "r") as file:
            json_data = file.read()
        try:
            question_list = json.loads(json_data)
            formatted_questions = format_helper.process_json_list(question_list)
            with open("temp/sample.txt", "a") as file:
                file.write(json.dumps(formatted_questions))
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            self.stdout.write(self.style.ERROR(f"JSON Decode Error: {e}"))

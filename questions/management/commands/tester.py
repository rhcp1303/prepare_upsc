from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import common_utils as helper
        helper.wrap_text_file("temp/py_2024.txt","temp/wrapped_2024.txt")

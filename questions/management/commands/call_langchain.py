from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import rag_langchain_helper as helper
        helper.call_langchain()
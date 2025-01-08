from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create embeddings for a pdf to be reused in langchain'

    def handle(self, *args, **options):
        from ... helpers import create_embeddings_helper as helper
        file_1 = "ancient_his.faiss"
        file_2 = "old_ancient.faiss"
        helper.merge_embeddings_and_store(file_1, file_2)
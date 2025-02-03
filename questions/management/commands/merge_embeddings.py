import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create embeddings for a pdf to be reused in vector search'

    def find_faiss_folders(self, path):
        faiss_folders = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".faiss"):
                    faiss_folders.append(root)
                    break
        print(faiss_folders)
        return list(set(faiss_folders))

    def handle(self, *args, **options):
        from ...helpers import embeddings_helper as helper
        base_url = "questions/data/faiss_files/consolidated_source_index/m"
        l = self.find_faiss_folders(base_url)
        helper.merge_embeddings_and_store(l)

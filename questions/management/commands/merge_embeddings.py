import os
from django.core.management.base import BaseCommand
from ...helpers import embeddings_helper as helper


class Command(BaseCommand):
    help = 'Merge embeddings for multiple pdfs to generate a consolidated faiss folder'

    def add_arguments(self, parser):
        parser.add_argument('--base_url', type=str,
                            help='path to the root folder containing faiss folders to be merged',
                            required=True)
        parser.add_argument('--embeddings_store_path', type=str,
                            help='path to the location where merged faiss folder is to be stored',
                            required=True)

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
        base_url = options['base_url']
        embeddings_store_path = options['embeddings_store_path']
        list_of_faiss_folders = self.find_faiss_folders(base_url)
        helper.merge_embeddings_and_store(list_of_faiss_folders, embeddings_store_path)

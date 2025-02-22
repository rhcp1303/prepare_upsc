from django.core.management.base import BaseCommand
from ...helpers import embeddings_helper as helper
import os


class Command(BaseCommand):
    help = 'Create embeddings (faiss folders) for generated mock mcq jsons for use in langchain query by user'

    def find_json_files(self, path):
        json_file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".json"):
                    json_file_list.append(root)
                    break
        print(json_file_list)
        return list(set(json_file_list))

    def add_arguments(self, parser):
        parser.add_argument('--base_url', type=str,
                            help='path to the root folder containing faiss folders to be merged',
                            required=True)
        parser.add_argument('--embeddings_store_path', type=str,
                            help='path to the location where merged faiss folder is to be stored',
                            required=True)

    def handle(self, *args, **options):
        base_url = options['base_url']
        embeddings_store_path = options['embeddings_store_path']
        list_of_json_files = self.find_json_files(base_url)
        helper.create_question_embeddings(list_of_json_files, embeddings_store_path)

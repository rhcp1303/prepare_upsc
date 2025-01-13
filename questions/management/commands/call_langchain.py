from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from ... helpers import rag_langchain_helper as helper
        prompt = """
        generate 10 upsc style mcqs from the provided text on environment current affairs of 2023  along 
        with correct option and detailed explanation and analysis option and important keywords and named entities in the 
        question. Also give short note on each of the important keywords and named entities in about 50 words each.
        
        one question should be of match the following pair type with the corresponding pairs jumbled up,
        one question should be of 2 statements type and requiring evaluation of it with four options,
        one question should be of single statement question based on factual recall with four options,
        one with multiple statements and requiring the correct ones to be chosen,
        make the questions so as to demand high factual recall,conceptual clarity, analytical skills,recall chronology,
    remember facts and data but dont give emphasis on data,
     ,application based and interdisciplinary in content ,
      dont make options differ based on figures and data,
    avoid vague, unclear and obvious statements in the question and
                 curate options so as to demand elimination techniques, identification, and remembering accurate concepts,data and facts,
                 and set moderate to high difficulty by giving lot of distractors by not giving obvious distant options to the actual answer,
                 also demand facts like literary source names, personality names, chronology
        """
        helper.call_langchain_to_generate_mcq(prompt)
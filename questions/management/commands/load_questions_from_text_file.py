import re
from langchain_google_genai import ChatGoogleGenerativeAI
import time
from django.core.management.base import BaseCommand
from ...helpers import (load_questions_from_pdf_helper as question_loader,
                        question_classifier_helper as classifier,
                        common_utils)
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyC_w68KVtMCloF5V3NKAUBp6EdhqcA0ylw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


class Command(BaseCommand):
    help = 'Extract questions from a txt file and ingest to database'

    def add_arguments(self, parser):
        parser.add_argument('text_file_path', type=str, help='path to the question paper text')
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        text_file_path = options['text_file_path']
        year = options['year']
        with open(text_file_path, "r") as file:
            text = file.read()
        question_dict = question_loader.extract_questions_from_text(text, "yes")
        data = []
        question_list = question_dict["list_of_question"]
        option_a_list = question_dict["list_of_option_a"]
        option_b_list = question_dict["list_of_option_b"]
        option_c_list = question_dict["list_of_option_c"]
        option_d_list = question_dict["list_of_option_d"]
        print("number of questions extracted: " + str(len(question_list)))
        print("number of option_a extracted: " + str(len(option_a_list)))
        print("number of option_b extracted: " + str(len(option_b_list)))
        print("number of option_c extracted: " + str(len(option_c_list)))
        print("number of option_d extracted: " + str(len(option_d_list)))
        for i in range(len(question_list)):
            regex_pattern_for_correct_option = r"correct_option:.*([a-d]).*(?=\n)"
            subject = classifier.classify_question(question_list[i])
            question_prompt = question_list[i] + "\n(a) " + option_a_list[i] + "\n(b) " + option_b_list[i] + "\n(c) " + \
                              option_c_list[i] + "\n(d) " + option_d_list[i] + "\n"
            try:
                response = llm.invoke(question_prompt).content
                correct_option = re.findall(regex_pattern_for_correct_option, response)[0]
                explanation = response
            except Exception as e:
                print(e)
                continue
            time.sleep(5)
            data.append({
                "Q.No.": i + 1,
                "question_text": question_list[i],
                "option_a": option_a_list[i],
                "option_b": option_b_list[i],
                "option_c": option_c_list[i],
                "option_d": option_d_list[i],
                "correct_option": correct_option,
                "subject": subject,
                "year": year,
                "explanation": explanation
            })
        common_utils.write_to_json(data, 'questions/data/upsc_questions/temp_question_data.json')

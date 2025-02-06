from langchain_google_genai import ChatGoogleGenerativeAI
import re
from ..helpers import question_classifier_helper as classifier
import time
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyC_w68KVtMCloF5V3NKAUBp6EdhqcA0ylw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


def extract_questions_from_text(extracted_text, extract_option):
    regex_pattern_for_question = r"\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    regex_pattern_for_answers = [r"\n\(a\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(b\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(c\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(d\)\s*(.*?)(?=\s*\n|$)"]
    question_list = re.findall(regex_pattern_for_question, extracted_text, re.DOTALL)
    if extract_option == 'no':
        return {"list_of_question": question_list}
    option_a_list = re.findall(regex_pattern_for_answers[0], extracted_text, re.DOTALL)
    option_b_list = re.findall(regex_pattern_for_answers[1], extracted_text, re.DOTALL)
    option_c_list = re.findall(regex_pattern_for_answers[2], extracted_text, re.DOTALL)
    option_d_list = re.findall(regex_pattern_for_answers[3], extracted_text, re.DOTALL)
    return {
        "list_of_question": question_list,
        "list_of_option_a": option_a_list,
        "list_of_option_b": option_b_list,
        "list_of_option_c": option_c_list,
        "list_of_option_d": option_d_list
    }


def create_pyq_dict(question_dict, year):
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
        return data

import re
from .pdf_utils import *


def extract_questions_from_text(extracted_text, extract_option):
    regex_pattern_for_question = r"\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    regex_pattern_for_answers = [r"\n\(a\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(b\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(c\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(d\)\s*(.*?)(?=\s*\n|$)"]
    question_list = re.findall(regex_pattern_for_question, extracted_text, re.DOTALL)
    print("------------------\n\n")
    print(question_list)
    print("-------------------\n\n")
    print("\n\nnumber of questions extracted: " + str(len(question_list)) + "\n\n")
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

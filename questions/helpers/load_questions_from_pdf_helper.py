import re
from .pdf_utils import *


def load_questions_from_pdf(pdf_file_path, pdf_type, extract_option='yes'):
    if pdf_type == 'scanned':
        extracted_text = TwoColumnScannedPDFExtractorUsingLLM().extract_text(pdf_file_path)
    else:
        extracted_text = TwoColumnDigitalPDFExtractor().extract_text(pdf_file_path)
    extracted_questions = extract_questions_from_text(extracted_text, extract_option)
    return extracted_questions


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
    answer_list_a = re.findall(regex_pattern_for_answers[0], extracted_text, re.DOTALL)
    answer_list_b = re.findall(regex_pattern_for_answers[1], extracted_text, re.DOTALL)
    answer_list_c = re.findall(regex_pattern_for_answers[2], extracted_text, re.DOTALL)
    answer_list_d = re.findall(regex_pattern_for_answers[3], extracted_text, re.DOTALL)
    return {
        "list_of_question": question_list,
        "list_of_option_a": answer_list_a,
        "list_of_option_b": answer_list_b,
        "list_of_option_c": answer_list_c,
        "list_of_option_d": answer_list_d
    }

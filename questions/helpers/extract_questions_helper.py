from langchain_google_genai import ChatGoogleGenerativeAI
import re
from ..helpers import question_classifier_helper as classifier
import time
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyC_w68KVtMCloF5V3NKAUBp6EdhqcA0ylw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


def extract_questions_from_text(extracted_text, extract_option):
    regex_pattern_for_question = r"\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    question_list = re.findall(regex_pattern_for_question, extracted_text, re.DOTALL)
    return {"list_of_question": question_list}


def extract_pyqs_from_text(extracted_text):
    regex_pattern_for_question = r"\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    regex_pattern_for_answers = [r"\n\(a\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(b\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(c\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(d\)\s*(.*?)(?=\s*\n|$)"]
    question_list = re.findall(regex_pattern_for_question, extracted_text, re.DOTALL)
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


def extract_mock_questions_from_text(extracted_text):
    regex_pattern_for_question_answer_explanation = r"(\*\*\d+\.\s*.*?)(?=\n\*\*\d+\.)"
    regex_pattern_for_question = r"\*\*\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    regex_pattern_for_options = [r"\n\(a\)\s*(.*?)(?=\n\(b\)\s*|$)",
                                 r"\n\(b\)\s*(.*?)(?=\n\(c\)\s*|$)",
                                 r"\n\(c\)\s*(.*?)(?=\n\(d\)\s*|$)",
                                 r"\n\(d\)\s*(.*?)(?=\*\*|$)"]
    regex_pattern_for_correct_option = r"\*\*Correct\s*Answer\s*:\s*\*\*\s*(.*?)(?=\s*\*\*|$)"
    regex_pattern_for_explanation = r"\*\*\s*Explanation\s*:\s*\*\*(.*?)(?=\s*\*\*\s*\d+\.|$)"
    question_answer_explanation_list = re.findall(regex_pattern_for_question_answer_explanation, extracted_text,
                                                  re.DOTALL)
    print("----------------------------")
    print(len(question_answer_explanation_list))
    print("----------------------------")
    question_list = []
    option_a_list = []
    option_b_list = []
    option_c_list = []
    option_d_list = []
    correct_option_list = []
    explanation_list = []
    for question_answer_explanation in question_answer_explanation_list:
        print(question_answer_explanation)
        question = re.findall(regex_pattern_for_question, question_answer_explanation, re.DOTALL)[0]
        option_a = re.findall(regex_pattern_for_options[0], question_answer_explanation, re.DOTALL)[0]
        option_b = re.findall(regex_pattern_for_options[1], question_answer_explanation, re.DOTALL)[0]
        option_c = re.findall(regex_pattern_for_options[2], question_answer_explanation, re.DOTALL)[0]
        option_d = re.findall(regex_pattern_for_options[3], question_answer_explanation, re.DOTALL)[0]
        correct_option = re.findall(regex_pattern_for_correct_option, question_answer_explanation, re.DOTALL)[0]
        explanation = re.findall(regex_pattern_for_explanation, question_answer_explanation, re.DOTALL)[0]
        question_list.append(question)
        option_a_list.append(option_a)
        option_b_list.append(option_b)
        option_c_list.append(option_c)
        option_d_list.append(option_d)
        correct_option_list.append(correct_option)
        explanation_list.append(explanation)

    return {
        "list_of_question": question_list,
        "list_of_option_a": option_a_list,
        "list_of_option_b": option_b_list,
        "list_of_option_c": option_c_list,
        "list_of_option_d": option_d_list,
        "list_of_correct_option": correct_option_list,
        "list_of_explanation": explanation_list
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
            "year": year,
            "q_num": i + 1,
            "subject": subject,
            "question_text": question_list[i],
            "option_a": option_a_list[i],
            "option_b": option_b_list[i],
            "option_c": option_c_list[i],
            "option_d": option_d_list[i],
            "correct_option": correct_option,
            "explanation": explanation
        })
        return data


def create_mock_mcq_dict(question_dict, pattern_type, subject, content_type):
    data = []
    question_list = question_dict["list_of_question"]
    option_a_list = question_dict["list_of_option_a"]
    option_b_list = question_dict["list_of_option_b"]
    option_c_list = question_dict["list_of_option_c"]
    option_d_list = question_dict["list_of_option_d"]
    correct_option_list = question_dict["list_of_correct_option"]
    explanation_list = question_dict["list_of_explanation"]
    print("number of questions extracted: " + str(len(question_list)))
    print("number of option_a extracted: " + str(len(option_a_list)))
    print("number of option_b extracted: " + str(len(option_b_list)))
    print("number of option_c extracted: " + str(len(option_c_list)))
    print("number of option_d extracted: " + str(len(option_d_list)))
    print("number of correct_options extracted: " + str(len(correct_option_list)))
    print("number of explanations extracted: " + str(len(explanation_list)))
    for i in range(len(question_list)):
        data.append({
            "subject": subject,
            "content_type": content_type,
            "pattern_type": pattern_type,
            "question_text": question_list[i],
            "option_a": option_a_list[i],
            "option_b": option_b_list[i],
            "option_c": option_c_list[i],
            "option_d": option_d_list[i],
            "correct_option": correct_option_list[i],
            "explanation": explanation_list[i]
        })
    return data

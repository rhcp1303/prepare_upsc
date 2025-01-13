import os
import re
from PIL import Image
import pdfplumber
from django.core.files.storage import default_storage
import google.generativeai as genai
from langdetect import detect


BASE_URL_PREFIX = "/Users/ankit.anand/PycharmProjects/PrepareUPSC/prepare_upsc"
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI")

def load_questions_from_pdf(pdf_file_path,pdf_type,extract_option='yes'):
    if pdf_type == 'scanned':
        extracted_text = extract_text_from_scanned_pdf(pdf_file_path)
    else:
        extracted_text = extract_text_from_pdf(pdf_file_path )
    extracted_questions = extract_questions_from_text(extracted_text,extract_option)
    return extracted_questions

def extract_text_from_pdf(pdf_file_path):
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                page_text = ""
                crop_box = (0, 0, page.width / 2, page.height)
                cropped_page = page.within_bbox(crop_box)
                page_text += cropped_page.extract_text()
                crop_box = (page.width / 2, 0, page.width, page.height)
                cropped_page = page.within_bbox(crop_box)
                page_text += cropped_page.extract_text()
                if page_text.find("a)") != -1:
                    extracted_text += page_text
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return extracted_text

def extract_text_from_scanned_pdf(pdf_file_path):

    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            all_text = ""
            for page_num, page in enumerate(pdf.pages):
                image_path = f"temp_page_{page_num}.png"
                page.to_image().save(image_path)
                img_url = BASE_URL_PREFIX + default_storage.url(image_path)
                img = Image.open(img_url)
                response = model.generate_content(["extract text from this image without any additional context or headers", img])
                text = response.text
                os.remove(f"temp_page_{page_num}.png")
                try:
                    detected_lang =  detect(text)
                    if detected_lang == "hi":
                        continue
                    if text.find("(a)") != -1:
                        all_text += text + "\n"
                except Exception as e:
                    print("error here")

            return all_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def extract_questions_from_text(extracted_text,extract_option):
    regex_pattern_for_question = r"\d+\.\s*(.*?)(?=\n\(a\)\s*|$)"
    regex_pattern_for_answers = [r"\n\(a\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(b\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(c\)\s*(.*?)(?=\s*\n|$)",
                                 r"\n\(d\)\s*(.*?)(?=\s*\n|$)"]

    question_list = re.findall(regex_pattern_for_question, extracted_text, re.DOTALL)
    print("------------------\n\n")
    print(question_list)
    print("-------------------\n\n")
    print("\n\nnumber of questions extracted: "+str(len(question_list))+"\n\n")
    if extract_option == 'no':
        return {"list_of_question":question_list}
    answer_list_a = re.findall(regex_pattern_for_answers[0], extracted_text, re.DOTALL)
    answer_list_b = re.findall(regex_pattern_for_answers[1], extracted_text, re.DOTALL)
    answer_list_c = re.findall(regex_pattern_for_answers[2], extracted_text, re.DOTALL)
    answer_list_d = re.findall(regex_pattern_for_answers[3], extracted_text, re.DOTALL)
    return {
        "list_of_question":question_list,
        "list_of_option_a":answer_list_a,
        "list_of_option_b":answer_list_b,
        "list_of_option_c":answer_list_c,
        "list_of_option_d":answer_list_d
    }
import json
import time
import pdfplumber
import google.generativeai as genai
from PIL import Image
import os
import pytesseract
from langdetect import detect
import typing_extensions as typing
from concurrent.futures import ProcessPoolExecutor

model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI")


def write_to_json(data, output_path):
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def merge_json_lists(list1_path, list2_path, output_file_path):
    try:
        with open(list1_path, 'r') as f1:
            list1 = json.load(f1)
        with open(list2_path, 'r') as f2:
            list2 = json.load(f2)
        if not isinstance(list1, list):
            raise ValueError("First file does not contain a JSON list.")
        if not isinstance(list2, list):
            raise ValueError("Second file does not contain a JSON list.")
        merged_list = list1 + list2
        with open(output_file_path, 'w') as outfile:
            json.dump(merged_list, outfile, indent=4)
        print(f"Successfully merged {list1_path} and {list2_path} into {output_file_path}")
    except FileNotFoundError:
        print(f"Error: One or both input files not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            print(page.extract_text())
    return text


def extract_text_from_scanned_pdf_using_gemini(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page_num, page in enumerate(pdf.pages):
                image_path = f"temp/temp_page_{page_num}.png"
                page.to_image(resolution=300).save(image_path)
                img = Image.open(image_path)
                try:
                    response = model.generate_content(
                        ["extract text from this image without any additional context or headers", img])
                except Exception as e:
                    print(f"Error processing page {page_num + 1}: {e}")
                    break
                time.sleep(5)
                text = response.text
                print(text)
                os.remove(image_path)
                all_text += text + "\n"
            return all_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""


def extract_text_from_page(page_number, pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        crop_box = (0, 0, page.width / 2, page.height)
        left_half_page = page.within_bbox(crop_box)
        left_half_image = left_half_page.to_image(resolution=300)
        left_half_image_path = f"temp/temp_left_half_page_{page.page_number}.jpg"
        left_half_image.save(left_half_image_path)
        left_extracted_text = pytesseract.image_to_string(left_half_image_path, lang='eng')
        print(left_extracted_text)
        crop_box = (page.width / 2, 0, page.width, page.height)
        right_half_page = page.within_bbox(crop_box)
        right_half_image = right_half_page.to_image(resolution=300)
        right_half_image_path = f"temp/temp_right_half_page_{page.page_number}.jpg"
        right_half_image.save(right_half_image_path)
        right_extracted_text = pytesseract.image_to_string(right_half_image_path, lang='eng')
        print(right_extracted_text)
        os.remove(left_half_image_path)
        os.remove(right_half_image_path)
        return left_extracted_text + "\n" + right_extracted_text


def extract_text_from_scanned_pdf(pdf_path):
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(extract_text_from_page,
                                    range(len(pdfplumber.open(pdf_path).pages)),
                                    [pdf_path] * len(pdfplumber.open(pdf_path).pages)))
    return "\n".join(filter(None, results))


def call_gemini_api_to_get_explanation(prompt):
    class Explanation(typing.TypedDict):
        correct_option: str
        explanation: str

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=Explanation
        ),
    )
    return response.text


def wrap_text_file(input_file, output_file, line_length=80):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.strip():
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= line_length:
                        current_line += word + " "
                    else:
                        f_out.write(current_line.strip() + "\n")
                        current_line = word + " "
                if current_line:
                    f_out.write(current_line.strip() + "\n")
            else:
                f_out.write("\n")


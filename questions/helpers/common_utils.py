import json
import time
import numpy as np
import pdfplumber
import csv
import google.generativeai as genai
from django.core.files.storage import default_storage
from PIL import Image
import os
import pytesseract
from langdetect import detect


BASE_URL_PREFIX = "/Users/ankit.anand/PycharmProjects/PrepareUPSC/prepare_upsc"
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI")

def write_to_json(data,output_path):
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def csv_to_json(csv_file, json_file):
  data = []
  with open(csv_file, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if(row):
            data.append({
                "question_text": row[0],
                "subject": row[1]
            })

  with open(json_file, 'w') as jsonfile:
    json.dump(data, jsonfile, indent=4)


def merge_embeddings(d1, centroid1, d2, method='concat'):
    if d1 != len(d2):
        raise ValueError("Embeddings must have the same dimensionality for merging.")
    if method == 'concat':
        return np.concatenate((centroid1, d2))
    elif method == 'average':
        return (centroid1 + d2) / 2
    elif method == 'sum':
        return centroid1 + d2
    else:
        raise ValueError(f"Invalid merge method: {method}")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_scanned_pdf_using_gemini(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page_num, page in enumerate(pdf.pages):
                image_path = f"temp_page_{page_num}.png"
                page.to_image().save(image_path)
                img_url = BASE_URL_PREFIX + default_storage.url(image_path)
                img = Image.open(img_url)
                response = model.generate_content(["extract text from this image without any additional context or headers", img])
                time.sleep(5)
                text = response.text
                os.remove(f"temp_page_{page_num}.png")
                all_text += text + "\n"
            return all_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def extract_text_from_scanned_pdf(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page_num, page in enumerate(pdf.pages):
      image = page.to_image()
      image.save(f"temp_page_{page_num}.png")
      extracted_text = pytesseract.image_to_string(f"temp_page_{page_num}.png",lang='hin+eng')
      lang = detect(extracted_text)
      if lang == 'hi':
          continue
      print(extracted_text)
      text += extracted_text + "\n"
      os.remove(f"temp_page_{page_num}.png")
  return text
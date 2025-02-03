import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import re

os.environ["GOOGLE_API_KEY"] = "AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key='AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI')

prompt_template_for_refining_single_stmt_type_question = ""

def refine_generated_mcq(text_file_path):
    with open(text_file_path, "r") as file:
        raw_question_text = file.read()
        regex_pattern_for_question = r"\*\*\d+\.\s*(.*?)(?=\*\*\d+\.)"
        raw_question_list = re.findall(regex_pattern_for_question, raw_question_text, re.DOTALL)
        print("---------------------------------------------------------------------------")
        print(f"number of questions extracted from raw text file: {len(raw_question_list)}")
        print("---------------------------------------------------------------------------")
        query=""
        for i in range(0, len(raw_question_list)):
            query+= "\n"+raw_question_list[i]
            if (i+1)%10 == 0:
                print(query)
                response = llm.invoke(query +"\n\n"+ prompt_template_for_refining_single_stmt_type_question).content
                with open("temp/refined_spectrum.txt","a+") as file:
                    file.write(response)
                query = ""
        response = llm.invoke(query + "\n\n" + prompt_template_for_refining_single_stmt_type_question).content
        with open("temp/refined_spectrum.txt", "a+") as file:
            file.write(response)

    return

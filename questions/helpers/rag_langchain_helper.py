from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

class MyOutputSchema(BaseModel):
    correct_option: str
    explanation: str

os.environ["GOOGLE_API_KEY"] = "AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def call_langchain(query):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("questions/data/faiss_files/complete.faiss",
                                   embeddings=embeddings,
                                   allow_dangerous_deserialization=True)
    prompt_template = """
    
**Question:** 
{question}
**Response:**
Return  the following in text format only :
* **correct_option:** the correct option in the given mcq.
* **explanation:** The explanation for the answer along with a short note on all the named entities (without giving any heading of 
 "named entities") in the given question and also options if they content important keywords and named entities from the 
 {context} from upsc exam preparation point of view without mentioning the context or information about the references from 
 the retrieved document. Don't  explicitly use topic name and chapter name from the context. Don't make guess. Also don't 
 mention if you don't know the result. Simply give an empty response in that case. Compile notes giving information 
 about anything and everything found in the document about the topic. Also give short note on each of the important keywords
  and named entities in about 50 words each

**Example:**
**Prompt:** 
18. Which one of the following National Parks lies completely in the temperate alpine zone?
(a) Manas National Park
(b) Namdapha National Park
(c) Neora Valley National Park
(d) Valley of Flowers National Park

**Response:**
correct_option: (d)
explanation: description about each of the national parks and short note on their geographical locations, features, etc.
"""


    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["question","context"]
    )


    qa_chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        prompt = prompt,

    )

    print(query)
    answer = qa_chain.run(query)
    print(answer)
    print("here")
    return answer


def call_langchain_to_generate_mcq(query):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("questions/data/faiss_files/complete.faiss",
                                   embeddings=embeddings,
                                   allow_dangerous_deserialization=True)
    prompt_template = """

**Prompt:** 
{query}
**Response:**
Return  the following in text format only :

* **question::** multiple choice question with four options in upsc style
* **correct_option:** the correct option in the given mcq.
* **explanation:** The explanation for the answer along with a short note on all the named entities (without giving any heading of 
 "named entities") in the given question and also options if they content important keywords and named entities from the 
 {context} from upsc examp preparation point of view without mentioning the context or information about the references from 
 the retrieved document. Don't  explicitly use topic name and chapter name from the context. Don't make guess. Also don't 
 mention if you don't know the result. Simply give an empty response in that case. Compile notes giving information 
 about anything and everything found in the document about the topic while also summarizing it.

**Example:**
**Prompt:** 
create a upsc style mcq from environment topic
**Response:**
question:Which one of the following National Parks lies completely in the temperate alpine zone?
(a) Manas National Park
(b) Namdapha National Park
(c) Neora Valley National Park
(d) Valley of Flowers National Park
correct_option: (d)
explanation: description about each of the national parks and short note on their geographical locations, features, etc.
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["query", "context"]
    )

    qa_chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever()
        # prompt=prompt,

    )

    print(query)
    answer = qa_chain.run(query)
    print(answer)
    return answer

def generate_mock_mcq(subject, topic, pattern_type, difficulty_level):
    return


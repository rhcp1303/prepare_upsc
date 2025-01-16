import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from ..helpers import common_utils as cu

os.environ["GOOGLE_API_KEY"] = "AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


def create_embeddings_and_store(pdf_file_path, embeddings_store_path):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    extracted_text = cu.extract_text_from_scanned_pdf(pdf_file_path)
    print(extracted_text)
    pdf_chunks = text_splitter.split_text(extracted_text)
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_texts(pdf_chunks, embeddings)
    vectorstore.save_local(embeddings_store_path)


def merge_embeddings_and_store(file_list):
    embeddings = HuggingFaceEmbeddings()
    vectorstore_1 = FAISS.load_local(file_list[0], embeddings=embeddings, allow_dangerous_deserialization=True)
    for i in range(1, len(file_list)):
        vectorstore_2 = FAISS.load_local(file_list[i], embeddings=embeddings, allow_dangerous_deserialization=True)
        vectorstore_1.merge_from(vectorstore_2)
    vectorstore_1.save_local("questions/data/faiss_files/complete.faiss")

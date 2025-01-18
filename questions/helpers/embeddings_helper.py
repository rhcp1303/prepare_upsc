import os

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from .pdf_utils import *


def create_embeddings_and_store(pdf_file_path, embeddings_store_path, pdf_type, number_of_columns, use_llm):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    if pdf_type == "scanned":
        if use_llm.lower() == 'yes':
            if number_of_columns == 1:
                extracted_text = SingleColumnScannedPDFExtractorUsingLLM().extract_text(pdf_file_path)
            else:
                extracted_text = TwoColumnScannedPDFExtractorUsingLLM().extract_text(pdf_file_path)
        else:
            if number_of_columns == 1:
                extracted_text = SingleColumnScannedPDFExtractorUsingOCR().extract_text(pdf_file_path)
            else:
                extracted_text = TwoColumnScannedPDFExtractorUsingOCR().extract_text(pdf_file_path)
    else:
        if number_of_columns == 1:
            extracted_text = SingleColumnDigitalPDFExtractor().extract_text(pdf_file_path)
        else:
            extracted_text = TwoColumnDigitalPDFExtractor().extract_text(pdf_file_path)

    print(extracted_text + "\n\n")
    print(len(extracted_text))
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

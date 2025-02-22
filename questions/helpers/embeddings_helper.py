from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import json
from langchain.docstore.document import Document


def create_embeddings_and_store(text, chunk_size, chunk_overlap, embeddings_store_path):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=".")
    pdf_chunks = text_splitter.split_text(text)
    print(f"number of pdf chunks created: {len(pdf_chunks)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore = FAISS.from_texts(pdf_chunks, embeddings)
    vectorstore.save_local(embeddings_store_path)


def merge_embeddings_and_store(folder_list, embeddings_store_path):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore_1 = FAISS.load_local(folder_list[0], embeddings=embeddings, allow_dangerous_deserialization=True)
    for i in range(1, len(folder_list)):
        print(folder_list[i])
        vectorstore_2 = FAISS.load_local(folder_list[i], embeddings=embeddings, allow_dangerous_deserialization=True)
        vectorstore_1.merge_from(vectorstore_2)
    vectorstore_1.save_local(embeddings_store_path)


def load_mcqs_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    documents = []
    for item in data:
        content = f"Question: {item['question_text']}\nOptions:\nA: {item['option_a']}\nB: {item['option_b']}\nC: {item['option_c']}\nD: {item['option_d']}\nAnswer: {item['correct_option']}\nExplanation: {item['explanation']}"
        metadata = {"subject": item['subject']}
        documents.append(Document(page_content=content, metadata=metadata))
    return documents


def create_question_embeddings(mcq_file_list, embeddings_store_path):
    all_documents = []
    for file in mcq_file_list:
        all_documents.extend(load_mcqs_from_json(file))
    print(f"Loaded {len(all_documents)} MCQs.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore = FAISS.from_documents(all_documents, embeddings)
    vectorstore.save_local(embeddings_store_path)

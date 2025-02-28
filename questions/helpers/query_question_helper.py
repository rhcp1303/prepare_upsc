import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
import random

def query_question(user_topic_query, num_questions):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    embeddings_store_path = "questions/data/faiss_folders/question.faiss"
    vectorstore = FAISS.load_local(embeddings_store_path, embeddings=embeddings,
                                   allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": num_questions})
    docs = retriever.get_relevant_documents(user_topic_query)
    retrieved_mcqs = []
    for i, doc in enumerate(docs):
        item = json.loads(doc.page_content)
        retrieved_mcqs.append(item)
        options = ['a', 'b', 'c', 'd']
        random.shuffle(options)
        option_mapping = {}
        for option in options:
            if option == 'a':
                option_mapping[option] = item['option_a']
            elif option == 'b':
                option_mapping[option] = item['option_b']
            elif option == 'c':
                option_mapping[option] = item['option_c']
            elif option == 'd':
                option_mapping[option] = item['option_d']
        for option in options:
            print(f"{option}. {option_mapping[option]}")
        print("\n\n")
    return retrieved_mcqs

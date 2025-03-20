from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import gradio as gr

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
embeddings_store_path = "questions/data/faiss_folders/consolidated_source_index/polity.faiss"
vectorstore = FAISS.load_local(embeddings_store_path, embeddings=embeddings,
                               allow_dangerous_deserialization=True)
api_key = "AIzaSyBq2_GdMf0KhowSVSb0hn4Z_8B81kBewXY"
os.environ["GOOGLE_API_KEY"] = api_key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


def query_question(user_topic_query):
    docs = vectorstore.similarity_search(user_topic_query)
    document_texts = [doc.page_content for doc in docs]
    combined_text = "\n\n".join(document_texts)
    prompt_template_str = """
                    Context:
                    {context}

                    Question: {question}

                    Answer:
                    """
    prompt = PromptTemplate(template=prompt_template_str, input_variables=["context", "question"])
    formatted_prompt = prompt.format(context=combined_text, question=user_topic_query)
    response = llm.invoke(formatted_prompt)
    return response.content


def gradio_interface(query):
    answer = query_question(query)
    return answer


iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(label="Enter your question"),
    outputs=gr.Textbox(label="Answer"),
    title="UPSC Question Answering System",
    description="Ask any question related to UPSC polity and get answers."
)

if __name__ == "__main__":
    iface.launch()
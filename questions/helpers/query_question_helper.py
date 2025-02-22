import gradio as gr
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


def query_question(user_topic_query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    embeddings_path = "questions/data/faiss_folders/question.faiss"
    try:
        vectorstore = FAISS.load_local(
            embeddings_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True)
    except Exception as e:
        return f"Error loading vectorstore: {e}"

    results = vectorstore.similarity_search_with_score(user_topic_query, k=5)
    output = ""
    question_number = 1
    for doc, score in results:
        output += f"Q. {question_number})\n"
        question = doc.page_content.replace("**", "\n")
        question = question.replace("\nOptions:\n", "\n")
        question = question.replace("\nA:", "\n(a)")
        question = question.replace("\nB:", "\n(b)")
        question = question.replace("\nC:", "\n(c)")
        question = question.replace("\nD:", "\n(d)")
        question = question.replace("Question:", "")

        output += f"{question}\n"
        output += "\n"
        question_number += 1
    return output


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            output_text = gr.Textbox(label="Questions", lines=20)

    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="Enter a topic or query")
            submit_btn = gr.Button("Submit")

    submit_btn.click(query_question, inputs=user_input, outputs=output_text)

demo.launch()

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyCxTCYQO7s23L33kC4Io4G-i1p1ytD-OiI"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def call_langchain():
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("temp_merged_faiss_index.faiss",
                                   embeddings=embeddings,
                                   allow_dangerous_deserialization=True)
    prompt_template = """
                **Question:** {question}

                **Relevant NCERT Text:** {context}

                **Instructions:**
                * Consider the provided NCERT text and answer the question based on it.
                * Provide a concise and informative answer.
                * Avoid overly complex or technical jargon.

                **Answer:**
                """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["question", "context"]
    )

    qa_chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        prompt=prompt
    )
    question = ("create 10 upsc style mcqs with 4 options each  from 'Iranian and Macedonian invasion' topic, where"
                "one question should be of match the following pair type with the corresponding pairs jumbled up,"
                " one question should be of 2 statements type and requiring evaluation of it with four options,"
                "one question should be of single statement question based on factual recall with four options,"
                "one multiple statements and requiring the correct ones,"
                "one with few option statements/objects that need to be selected as per the question statement,"
                "make the questions so a s to demand high conceptual clarity, analytical skills,recall chronology,"
                "remember facts and data but not dates,application based and interdisciplinary in content "
                " avoid vague, unclear and obvious statements in the question and"
                "curate options so as to demand elimination techniques, identification, and remembering accurate concepts,data and facts,"
                )
    print(question)
    answer = qa_chain.run(question)
    print(answer)

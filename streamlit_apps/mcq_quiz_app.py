import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from questions.helpers import query_question_helper as helper

st.set_page_config(
    page_title="MCQ Quiz App",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main .block-container {
        background-color: #333333; /* Dark gray */
        color: #FFFFFF; /* White text for contrast */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MCQ Quiz App")
user_query = st.text_input("Enter your query (e.g., 'Indian Polity', 'Capital cities', etc.):")
if "retrieved_questions" not in st.session_state:
    st.session_state.retrieved_questions = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "option_mappings" not in st.session_state:
    st.session_state.option_mappings = {}
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
num_questions = 5
if st.button("Start Quiz"):
    if user_query:
        with st.spinner("Loading questions..."):
            try:
                st.session_state.retrieved_questions = helper.query_question(user_query, num_questions)
                st.session_state.user_answers = {}
                st.session_state.quiz_started = True
                st.session_state.quiz_finished = False
                st.session_state.option_mappings = {}
                for question in st.session_state.retrieved_questions:
                    options = ['a', 'b', 'c', 'd']
                    option_mapping = {}
                    for option in options:
                        if option == 'a':
                            option_mapping[option] = question['option_a']
                        elif option == 'b':
                            option_mapping[option] = question['option_b']
                        elif option == 'c':
                            option_mapping[option] = question['option_c']
                        elif option == 'd':
                            option_mapping[option] = question['option_d']
                    st.session_state.option_mappings[question['question_text']] = option_mapping
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
if st.session_state.quiz_started:
    if not st.session_state.quiz_finished:
        for i, question in enumerate(st.session_state.retrieved_questions):
            st.write(f"Q. {i + 1})\n\n{question['question_text'].replace('**', ' ')}")
            option_mapping = st.session_state.option_mappings[question['question_text']]
            options = list(option_mapping.keys())
            display_options = {}
            for opt in options:
                display_options[opt] = option_mapping[opt]
            for option in options:
                if st.button(display_options[option], key=f"q{i}_button_{option}", use_container_width=True):
                    st.session_state.user_answers[i] = option
                    for o in options:
                        if o != option and f"q{i}_selected_{o}" in st.session_state:
                            del st.session_state[f"q{i}_selected_{o}"]
                    st.session_state[f"q{i}_selected_{option}"] = True
        if st.button("Submit Quiz"):
            st.session_state.quiz_finished = True
    elif st.session_state.quiz_finished:
        score = 0
        correct_count = 0
        incorrect_count = 0
        unattempted_count = 0
        attempted_count = 0

        st.markdown("""
        <style>
        .correct {
            background-color: lightgreen !important;
            color: black !important;
            border: none;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 5px;
        }
        .incorrect {
            background-color: lightcoral !important;
            color: black !important;
            border: none;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 5px;
        }
        button {
            border: none;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        for i, question in enumerate(st.session_state.retrieved_questions):
            st.write(f"Q. {i + 1}) {question['question_text'].replace('**', ' ')}")

            correct_answer_letter = question['correct_option'].replace("(", "").replace(")", "").upper()
            actual_correct_answer_text = question[f"option_{correct_answer_letter.lower()}"]
            actual_correct_answer = None
            for key, value in st.session_state.option_mappings[question['question_text']].items():
                if value == actual_correct_answer_text:
                    actual_correct_answer = key
                    break
            option_mapping = st.session_state.option_mappings[question['question_text']]
            options = list(option_mapping.keys())
            display_options = {}
            for opt in options:
                display_options[opt] = option_mapping[opt]
            for option in options:
                class_name = ""
                if option == actual_correct_answer:
                    class_name = "correct"
                elif option == st.session_state.user_answers.get(i) == option and option != actual_correct_answer:
                    class_name = "incorrect"
                st.markdown(f"""
                <button class="{class_name}" disabled>{display_options[option]}</button>
                """, unsafe_allow_html=True)
            st.write(f"Your answer: {st.session_state.user_answers.get(i, 'Not answered')}")
            st.write(f"Correct answer: {actual_correct_answer} ({actual_correct_answer_text})")
            st.write(f"Explanation: {question['explanation']}")
            if st.session_state.user_answers.get(i) == actual_correct_answer:
                score += 2
                correct_count += 1
                attempted_count += 1
            elif st.session_state.user_answers.get(i) and st.session_state.user_answers.get(i) != actual_correct_answer:
                score -= 2/3
                incorrect_count += 1
                attempted_count += 1
            else:
                unattempted_count += 1
            st.write("---")
        st.subheader("Quiz Results")
        st.write(f"**You scored {score:.2f} marks.**")
        st.write(f"Correct Answers: {correct_count}")
        st.write(f"Incorrect Answers: {incorrect_count}")
        st.write(f"Attempted Answers: {attempted_count}")
        st.write(f"Unattempted Answers: {unattempted_count}")

        if st.button("Start New Quiz"):
            st.session_state.clear()
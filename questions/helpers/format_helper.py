import textwrap


def format_question(question_data):
    question_text = question_data["question_text"]
    lines = question_text.split("\n")
    formatted_lines = []
    wrap_width = 80
    for line in lines:
        line = line.strip()
        if not line:
            continue
        wrapped_lines = textwrap.wrap(line, width=wrap_width)
        for i, wrapped_line in enumerate(wrapped_lines):
            if i > 0 and (lines[lines.index(line.strip())].strip().startswith(tuple(f"{n}." for n in range(1, 10)))):
                formatted_lines.append("   " + wrapped_line)
            else:
                formatted_lines.append(wrapped_line)
    formatted_question_string = "\n".join(formatted_lines)
    formatted_question_data = {
        "question_text": formatted_question_string,
        "option_a": question_data.get("option_a"),
        "option_b": question_data.get("option_b"),
        "option_c": question_data.get("option_c"),
        "option_d": question_data.get("option_d"),
        "correct_option": question_data.get("correct_option", None),
        "explanation": question_data.get("explanation", None)
    }
    return formatted_question_data


def process_json_list(json_list):
    formatted_questions = []
    for question_data in json_list:
        formatted_questions.append(format_question(question_data))
    print(formatted_questions)
    return formatted_questions

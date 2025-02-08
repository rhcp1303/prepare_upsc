from pydantic_core._pydantic_core import ValidationError
from ..models import MockMCQ
import json


def get_correct_option(text):
    if '(a)' in text:
        return 'a'
    if '(b)' in text:
        return 'b'
    if '(c)' in text:
        return 'c'
    if '(d)' in text:
        return 'd'
    raise Exception


def load_questions_into_db_from_json(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data.")

    for question_data in data:
        print(question_data)
        try:
            MockMCQ.objects.create(
                subject=question_data['subject'],
                question_content_type=question_data['content_type'],
                pattern_type=question_data['pattern_type'],
                question_text=question_data['question_text'],
                option_a=question_data['option_a'],
                option_b=question_data['option_b'],
                option_c=question_data['option_c'],
                option_d=question_data['option_d'],
                explanation=question_data['explanation'],
                correct_option=get_correct_option(question_data['correct_option'])
            )
        except Exception as e:
            continue
        except (ValidationError, KeyError) as e:
            raise ValidationError(f"Error processing question: {e}")

    return

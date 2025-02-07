from pydantic_core._pydantic_core import ValidationError
from ..models import MockMCQ
import json


def load_questions_into_db_from_json(json_data, subject, question_type):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data.")

    for question_data in data:
        try:
            explanation = question_data['explanation']
            correct_option = question_data['correct_option']
            MockMCQ.objects.create(
                subject=subject,
                question_type=question_type,
                pattern_type=question_data['pattern_type'],
                question_text=question_data['question_text'],
                option_a=question_data['option_a'],
                option_b=question_data['option_b'],
                option_c=question_data['option_c'],
                option_d=question_data['option_d'],
                correct_option=correct_option,
                explanation=explanation,
            )
        except (ValidationError, KeyError) as e:
            raise ValidationError(f"Error processing question: {e}")

    return

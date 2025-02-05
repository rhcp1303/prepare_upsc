from pydantic_core._pydantic_core import ValidationError
from ..helpers.common_utils import SubjectCode
from ..models import PYQuestions
from django.db import transaction
import json


def load_questions_from_json(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data.")

    print(data)

    subject_mapping = {
        "history_art_and_culture": SubjectCode.HISTORY_ART_AND_CULTURE.value,
        "modern_indian_history": SubjectCode.MODERN_INDIAN_HISTORY.value,
        "economy": SubjectCode.ECONOMICS.value,
        "environment": SubjectCode.ENVIRONMENT.value,
        "science_and_technology": SubjectCode.SCIENCE_AND_TECH.value,
        "polity": SubjectCode.POLITY.value,
        "geography": SubjectCode.GEOGRAPHY.value,
    }

    for question_data in data:
        with transaction.atomic():
            try:
                subject_name = question_data.get('subject')
                subject = subject_mapping.get(subject_name)
                if not subject:
                    raise ValidationError(f"Invalid subject: {subject_name}")
                explanation = question_data['explanation']
                correct_option = question_data['correct_option']
                PYQuestions.objects.create(
                    year=question_data['year'],
                    q_num=question_data.get('Q.No.'),
                    subject=subject,
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

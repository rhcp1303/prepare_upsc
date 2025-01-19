from pydantic_core._pydantic_core import ValidationError
from ..helpers.common_utils import SubjectCode
from ..models import PYQuestions, PYQOptions, PYQExplanations
from django.db import transaction
import json


def load_questions_from_json(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data.")

    subject_mapping = {
        "history_art_and_culture": SubjectCode.HISTORY_ART_AND_CULTURE.value,
        "modern_indian_history": SubjectCode.MODERN_INDIAN_HISTORY.value,
        "economy": SubjectCode.ECONOMICS.value,
        "environment": SubjectCode.ENVIRONMENT.value,
        "science_and_technology": SubjectCode.SCIENCE_AND_TECH.value,
        "polity": SubjectCode.POLITY.value,
        "geography": SubjectCode.GEOGRAPHY.value,
        "international_relations": SubjectCode.INTERNATIONAL_RELATIONS.value
    }

    for question_data in data:
        with transaction.atomic():
            try:
                subject_name = question_data.get('subject')
                subject = subject_mapping.get(subject_name)
                if not subject:
                    raise ValidationError(f"Invalid subject: {subject_name}")

                explanation = PYQExplanations.objects.create(
                    explanation_text=question_data['explanation']
                )

                question = PYQuestions.objects.create(
                    subject=subject,
                    question_text=question_data['question_text'],
                    year=question_data['year'],
                    q_num=question_data.get('Q.No.'),
                    explanation=explanation
                )

                correct_option = question_data['correct_option']
                PYQOptions.objects.create(
                    question=question,
                    option_text=question_data['option_a'],
                    is_correct=(correct_option == 'a'),
                    option_num=1
                )
                PYQOptions.objects.create(
                    question=question,
                    option_text=question_data['option_b'],
                    is_correct=(correct_option == 'b'),
                    option_num=2
                )
                PYQOptions.objects.create(
                    question=question,
                    option_text=question_data['option_c'],
                    is_correct=(correct_option == 'c'),
                    option_num=3
                )
                PYQOptions.objects.create(
                    question=question,
                    option_text=question_data['option_d'],
                    is_correct=(correct_option == 'd'),
                    option_num=4
                )

            except (ValidationError, KeyError) as e:
                raise ValidationError(f"Error processing question: {e}")

    return

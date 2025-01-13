from pydantic_core._pydantic_core import ValidationError
from ..models import Subjects, PYQuestion, Options, Explanation
import json


def load_questions_from_json(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data.")

    subject_mapping = {
        "history_art_and_culture": Subjects.HISTORY_ART_AND_CULTURE,
        "modern_indian_history": Subjects.MODERN_INDIAN_HISTORY,
        "economy": Subjects.ECONOMICS,
        "environment": Subjects.ENVIRONMENT,
        "science_and_technology": Subjects.SCIENCE_AND_TECH,
        "polity": Subjects.POLITY,
        "geography": Subjects.GEOGRAPHY,
        "international_relations": Subjects.INTERNATIONAL_RELATIONS
    }

    for question_data in data:
        try:
            subject_name = question_data.get('subject')
            try:
                subject = subject_mapping.get(subject_name)
                if subject is None:
                    raise ValidationError(f"Invalid subject: {subject_name}")
            except KeyError:
                raise ValidationError(f"Invalid subject: {subject_name}")

            question = PYQuestion.objects.create(
                subject=subject.value,
                question_text=question_data['question_text'],
                year=question_data['year'],
                q_num=question_data.get('Q.No.')
            )
            correct_option = question_data['correct_option']
            option_a = Options.objects.create(
                question=question,
                option_text=question_data['option_a'],
                is_correct=(correct_option == 'a'),
                option_num=1
            )
            option_b = Options.objects.create(
                question=question,
                option_text=question_data['option_b'],
                is_correct=(correct_option == 'b'),
                option_num=2
            )
            option_c = Options.objects.create(
                question=question,
                option_text=question_data['option_c'],
                is_correct=(correct_option == 'c'),
                option_num=3
            )
            option_d = Options.objects.create(
                question=question,
                option_text=question_data['option_d'],
                is_correct=(correct_option == 'd'),
                option_num=4
            )
            explanation = Explanation.objects.create(
                question=question,
                explanation_text=question_data['explanation']
            )

        except KeyError as e:
            raise ValidationError(f"Missing required field: {e}")

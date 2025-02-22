from .models import MockMCQ
import random
from .helpers.common_utils import PatternType


def get_mock_mcq(subject_quotas, num_questions=100):
    all_questions = []
    for subject, category_quotas in subject_quotas.items():
        if sum(category_quotas.values()) <= 0:
            continue
        for category, quota in category_quotas.items():
            questions_per_pattern = quota // len(PatternType)
            subject_questions = []
            for pattern_type in PatternType:
                questions = MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                   question_content_type=category).order_by('?')[:questions_per_pattern]
                subject_questions.extend(questions)
            all_questions.extend(subject_questions)
    remaining_questions = num_questions - sum(
        len(list(
            MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value, question_content_type=category)))
        for
        subject, category_quotas in subject_quotas.items() for category, quota in category_quotas.items() for
        pattern_type in PatternType)
    if remaining_questions > 0:
        for subject, category_quotas in subject_quotas.items():
            for category, quota in category_quotas.items():
                for pattern_type in PatternType:
                    questions_to_add = min(remaining_questions,
                                           MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                                  question_content_type=category).count())
                    additional_questions = MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                                  question_content_type=category).order_by('?')[
                                           :questions_to_add]
                    all_questions.extend(additional_questions)
                    remaining_questions -= questions_to_add
                    if remaining_questions == 0:
                        break
                if remaining_questions == 0:
                    break
            if remaining_questions == 0:
                break
    start_index = 0
    for subject, category_quotas in subject_quotas.items():
        for category, quota in category_quotas.items():
            end_index = start_index + sum(
                len(list(MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                question_content_type=category)))
                for pattern_type in PatternType)
            random.shuffle(all_questions[start_index:end_index])
            start_index = end_index
    all_questions = all_questions[:num_questions]
    return all_questions

from math import remainder

from .models import MockMCQ
from .helpers.common_utils import PatternType


def get_mock_mcq(subject_quotas):
    all_questions = []
    for subject, category_quotas in subject_quotas.items():
        if sum(category_quotas.values()) <= 0:
            continue
        for category, quota in category_quotas.items():
            questions_per_pattern = quota // len(PatternType)
            remainder = quota - questions_per_pattern * len(PatternType)
            subject_questions = []
            for pattern_type in PatternType:
                questions = MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                   question_content_type=category).order_by('?')[:questions_per_pattern]
                subject_questions.extend(questions)
            for pattern_type in PatternType:
                if remainder > 0:
                    questions = MockMCQ.objects.filter(subject=subject, pattern_type=pattern_type.value,
                                                       question_content_type=category).order_by('?')[:1]
                    subject_questions.extend(questions)
                    remainder -= 1
            all_questions.extend(subject_questions)
    return all_questions

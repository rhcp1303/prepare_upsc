from django.test import TestCase
from ..models import PYQuestions
from ..helpers.common_utils import SubjectCode


class PYQuestionModelTest(TestCase):

    def setUp(self):
        self.subject_choice = str(SubjectCode.MODERN_INDIAN_HISTORY)

    def test_pyquestion_creation(self):
        pyquestion = PYQuestions.objects.create(
            year=2023,
            q_num=1,
            subject=self.subject_choice,
            question_text="Sample Question",
            option_a="option a",
            option_b="option b",
            option_c="option c",
            option_d="option d",
            correct_option="a",
            explanation="This is the explanation."

        )
        self.assertIsInstance(pyquestion, PYQuestions)

    def test_str_method(self):
        pyquestion = PYQuestions.objects.create(
            year=2023,
            q_num=1,
            subject=self.subject_choice,
            question_text="Sample Question",
            option_a="option a",
            option_b="option b",
            option_c="option c",
            option_d="option d",
            correct_option="a",
            explanation="This is the explanation."
        )
        self.assertEqual(str(pyquestion), "This is a sample question with a long text...")

    def test_ordering(self):
        pyquestion1 = PYQuestions.objects.create(
            year=2023,
            q_num=1,
            subject=self.subject_choice,
            question_text="Sample Question",
            option_a="option a",
            option_b="option b",
            option_c="option c",
            option_d="option d",
            correct_option="a",
            explanation="This is the explanation."
        )
        pyquestion2 = PYQuestions.objects.create(
            year=2021,
            q_num=5,
            subject=self.subject_choice,
            question_text="Sample Question",
            option_a="option a",
            option_b="option b",
            option_c="option c",
            option_d="option d",
            correct_option="a",
            explanation="This is the explanation."
        )
        pyquestions = PYQuestions.objects.all()
        self.assertEqual(list(pyquestions), [pyquestion1, pyquestion2])

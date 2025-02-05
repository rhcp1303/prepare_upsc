from django.test import TestCase
from ..models import PYQuestions
from ..helpers.common_utils import SubjectCode


class PYQuestionModelTest(TestCase):

    def setUp(self):
        self.subject_choice = str(SubjectCode.MODERN_INDIAN_HISTORY)

    def test_pyquestion_creation(self):
        pyquestion = PYQuestions.objects.create(
            subject=self.subject_choice,
            question_text="Sample Question",
            year=2023,
            q_num=1
        )
        self.assertIsInstance(pyquestion, PYQuestions)

    def test_str_method(self):
        pyquestion = PYQuestions.objects.create(
            subject=self.subject_choice,
            question_text="This is a sample question with a long text",
            year=2023,
            q_num=1
        )
        self.assertEqual(str(pyquestion), "This is a sample question with a long text...")

    def test_ordering(self):
        pyquestion1 = PYQuestions.objects.create(
            subject=self.subject_choice,
            question_text="Question 1",
            year=2022,
            q_num=5
        )
        pyquestion2 = PYQuestions.objects.create(
            subject=self.subject_choice,
            question_text="Question 2",
            year=2023,
            q_num=1
        )
        pyquestions = PYQuestions.objects.all()
        self.assertEqual(list(pyquestions), [pyquestion1, pyquestion2])

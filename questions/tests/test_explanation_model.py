from django.test import TestCase
from ..models import Explanations, PYQuestions


class ExplanationModelTest(TestCase):
    def setUp(self):
        self.pyquestion = PYQuestions.objects.create(question_text="Sample Question", year=2011, q_num=10)

    def test_explanation_creation(self):
        explanation = Explanations.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertIsInstance(explanation, Explanations)

    def test_question_relationship(self):
        explanation = Explanations.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertEqual(explanation.question, self.pyquestion)
        self.assertIn(explanation, self.pyquestion.explanation.all())

    def test_str_method(self):
        explanation = Explanations.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertEqual(str(explanation), "This is an explanation.")

    def test_cascade_deletion(self):
        explanation = Explanations.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.pyquestion.delete()
        self.assertFalse(Explanations.objects.filter(id=explanation.id).exists())

from django.test import TestCase
from ..models import Explanation, PYQuestion


class ExplanationModelTest(TestCase):
    def setUp(self):
        self.pyquestion = PYQuestion.objects.create(question_text="Sample Question", year=2011, q_num=10)

    def test_explanation_creation(self):
        explanation = Explanation.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertIsInstance(explanation, Explanation)

    def test_question_relationship(self):
        explanation = Explanation.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertEqual(explanation.question, self.pyquestion)
        self.assertIn(explanation, self.pyquestion.explanation.all())

    def test_str_method(self):
        explanation = Explanation.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.assertEqual(str(explanation), "This is an explanation.")

    def test_cascade_deletion(self):
        explanation = Explanation.objects.create(
            question=self.pyquestion,
            explanation_text="This is an explanation."
        )
        self.pyquestion.delete()
        self.assertFalse(Explanation.objects.filter(id=explanation.id).exists())

from django.test import TestCase
from ..models import PYQOptions, PYQuestions

class OptionsModelTest(TestCase):
    def setUp(self):
        self.pyquestion = PYQuestions.objects.create(question_text="Sample Question", year=2011, q_num=10)

    def test_option_creation(self):
        option = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertIsInstance(option, PYQOptions)

    def test_question_relationship(self):
        option = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertEqual(option.question, self.pyquestion)

    def test_str_method(self):
        option = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertEqual(str(option), "Option A")

    def test_ordering(self):
        option1 = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        option2 = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option B",
            is_correct=False,
            option_num=2
        )
        options = PYQOptions.objects.filter(question=self.pyquestion)
        self.assertEqual(list(options), [option1, option2])

    def test_cascade_deletion(self):
        option = PYQOptions.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.pyquestion.delete()
        self.assertFalse(PYQOptions.objects.filter(id=option.id).exists())
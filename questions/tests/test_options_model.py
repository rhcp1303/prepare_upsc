from django.test import TestCase
from ..models import Options, PYQuestion

class OptionsModelTest(TestCase):
    def setUp(self):
        self.pyquestion = PYQuestion.objects.create(question_text="Sample Question", year=2011, q_num=10)

    def test_option_creation(self):
        option = Options.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertIsInstance(option, Options)

    def test_question_relationship(self):
        option = Options.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertEqual(option.question, self.pyquestion)

    def test_str_method(self):
        option = Options.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.assertEqual(str(option), "Option A")

    def test_ordering(self):
        option1 = Options.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        option2 = Options.objects.create(
            question=self.pyquestion,
            option_text="Option B",
            is_correct=False,
            option_num=2
        )
        options = Options.objects.filter(question=self.pyquestion)
        self.assertEqual(list(options), [option1, option2])

    def test_cascade_deletion(self):
        option = Options.objects.create(
            question=self.pyquestion,
            option_text="Option A",
            is_correct=True,
            option_num=1
        )
        self.pyquestion.delete()
        self.assertFalse(Options.objects.filter(id=option.id).exists())
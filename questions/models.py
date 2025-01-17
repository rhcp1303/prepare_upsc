from django.db import models
from django.core.exceptions import ValidationError


class Subjects(models.TextChoices):
    MODERN_INDIAN_HISTORY = "MIH", "Modern Indian History"
    HISTORY_ART_AND_CULTURE = "HAC", "History, Art & Culture"
    POLITY = "POL", "Polity"
    INTERNATIONAL_RELATIONS = "IR", "International Relations"
    ECONOMICS = "ECO", "Economics"
    SCIENCE_AND_TECH = "ST", "Science & Technology"
    ENVIRONMENT = "ENV", "Environment"
    GEOGRAPHY = "GEO", "Geography"
    MISCELLANEOUS = "MISC", "Miscellaneous"


class Explanation(models.Model):
    explanation_text = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'prelims_explanation'

    def __str__(self):
        return self.explanation_text

    def __str__(self):
        return self.option_text


class PYQuestion(models.Model):
    subject = models.CharField(max_length=4, choices=Subjects.choices)
    question_text = models.TextField(null=False, blank=False)
    year = models.PositiveIntegerField(null=False)
    q_num = models.PositiveIntegerField(null=False)
    explanation = models.OneToOneField('Explanation', on_delete=models.CASCADE, related_name='question')

    class Meta:
        ordering = ['year', 'q_num']
        db_table = 'prelims_pyq'
        unique_together = ('year', 'q_num')

    def __str__(self):
        return self.question_text[:50] + "..."

    def clean(self):
        if self.options.count() != 4:
            raise ValidationError("Question must have exactly 4 options.")

        num_questions_per_year = PYQuestion.objects.filter(year=self.year).count()
        if num_questions_per_year >= 100:
            raise ValidationError("Cannot exceed 100 questions per year")


class Options(models.Model):
    question = models.ForeignKey(PYQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField(null=False, blank=False)
    is_correct = models.BooleanField(default=False, null=False)
    option_num = models.PositiveIntegerField(null=False)

    class Meta:
        ordering = ['option_num']
        db_table = 'prelims_options'
        unique_together = ('question', 'option_num')

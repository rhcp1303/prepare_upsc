from django.db import models


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

class PYQuestions(models.Model):
    subject = models.CharField(max_length=4, choices=Subjects.choices)
    question_text = models.TextField(null=False, blank=False)
    year = models.PositiveIntegerField(null=False)
    q_num = models.PositiveIntegerField(null=False)
    explanation = models.OneToOneField('Explanations', on_delete=models.CASCADE, related_name='question')

    class Meta:
        ordering = ['year', 'q_num']
        db_table = 'prelims_pyqs'
        unique_together = ('year', 'q_num')

    def __str__(self):
        return self.question_text[:50] + "..."


class Options(models.Model):
    question = models.ForeignKey(PYQuestions, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField(null=False, blank=False)
    is_correct = models.BooleanField(default=False, null=False)
    option_num = models.PositiveIntegerField(null=False)

    class Meta:
        ordering = ['option_num']
        db_table = 'prelims_options'
        unique_together = ('question', 'option_num')

        def __str__(self):
            return self.option_text


class Explanations(models.Model):
    explanation_text = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'prelims_explanations'

    def __str__(self):
        return self.explanation_text



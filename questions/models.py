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

class PYQuestion(models.Model):
    subject = models.CharField(max_length=4, choices=Subjects.choices)
    question_text = models.TextField()
    year = models.PositiveIntegerField()
    q_num = models.PositiveIntegerField()

    class Meta:
        ordering = ['year', 'q_num']
        db_table = 'prelims_pyq'

    def __str__(self):
        return self.question_text[:50] + "..."

class Options(models.Model):
    question = models.ForeignKey(PYQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    option_num = models.PositiveIntegerField()

    class Meta:
        ordering = ['option_num']
        db_table = 'prelims_options'

    def __str__(self):
        return self.option_text

class Explanation(models.Model):
    question = models.ForeignKey(PYQuestion, on_delete=models.CASCADE, related_name='explanation')
    explanation_text = models.TextField()

    class Meta:
        db_table = 'prelims_explanation'

    def __str__(self):
        return self.explanation_text
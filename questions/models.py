from django.db import models

class Subjects:
    ANCIENT_HISTORY = "Ancient History"
    MEDIEVAL_HISTORY = "Medieval History"
    MODERN_HISTORY = "Modern History"
    ART_AND_CULTURE = "Art & Culture"
    POLITY = "Polity"
    INTERNATIONAL_RELATIONS = "International Relations"
    ECONOMICS = "Economics"
    SCIENCE_AND_TECH = "Science & Technology"
    ENVIRONMENT = "Environment"
    GEOGRAPHY = "Geography"


class Question(models.Model):
    subject = models.CharField(max_length=50)
    question_text = models.TextField()
    year = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['year', 'order']

    def __str__(self):
        return self.question_text[:50] + "..."

class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

from django.db import models
from .helpers import common_utils as cu


class PYQuestions(models.Model):
    year = models.PositiveIntegerField(null=False)
    q_num = models.PositiveIntegerField(null=False)
    subject = models.CharField(max_length=4, choices=[(code.value, code.name) for code in cu.SubjectCode])
    question_text = models.TextField(null=False, blank=False)
    option_a = models.TextField(null=False, blank=False)
    option_b = models.TextField(null=False, blank=False)
    option_c = models.TextField(null=False, blank=False)
    option_d = models.TextField(null=False, blank=False)
    correct_option = models.CharField(max_length=1, choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
    explanation = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['year', 'q_num']
        db_table = 'prelims_pyqs'
        unique_together = ('year', 'q_num')

    def __str__(self):
        return self.question_text[:50] + "..."


class MockMCQ(models.Model):
    subject = models.CharField(max_length=4, choices=[(code.value, code.name) for code in cu.SubjectCode])
    question_content_type = models.CharField(max_length=6,
                                     choices=[(question_content_type.value, question_content_type.name) for
                                              question_content_type in
                                              cu.QuestionContentType])
    pattern_type = models.CharField(max_length=20, choices=[(pattern_type.value, pattern_type.name) for pattern_type in
                                                            cu.PatternType])
    question_text = models.TextField(null=False, blank=False)
    option_a = models.TextField(null=False, blank=False)
    option_b = models.TextField(null=False, blank=False)
    option_c = models.TextField(null=False, blank=False)
    option_d = models.TextField(null=False, blank=False)
    correct_option = models.CharField(max_length=1, choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
    explanation = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['pattern_type']
        db_table = 'prelims_mock_mcq'

    def __str__(self):
        return self.question_text[:50] + "..."

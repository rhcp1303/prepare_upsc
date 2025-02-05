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


class BaseMockMCQ(models.Model):
    question_text = models.TextField(null=False, blank=False)
    pattern_type = models.CharField(max_length=20, choices=[(pattern_type.value, pattern_type.name) for pattern_type in
                                                            cu.PatternType])
    option_a = models.TextField(null=False, blank=False)
    option_b = models.TextField(null=False, blank=False)
    option_c = models.TextField(null=False, blank=False)
    option_d = models.TextField(null=False, blank=False)
    explanation = models.TextField(null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ['pattern_type']

    def __str__(self):
        return self.question_text[:50] + "..."


class ModernIndianHistoryMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_history'


class HistoryArtAndCultureMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_history_art_and_culture'


class GeographyMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_geography'


class PolityMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_polity'


class EconomicsMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_economics'


class ScienceAndTechMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_science_and_tech'


class EnvironmentMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcqs_environment'


class CurrentAffairsMockMCQ(BaseMockMCQ):
    subject = models.CharField(max_length=4, choices=[(code.value, code.name) for code in cu.SubjectCode])

    class Meta:
        db_table = 'prelims_mock_mcq_current_affairs'

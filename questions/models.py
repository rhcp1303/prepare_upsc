from django.db import models
from .helpers import common_utils as cu
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BaseOptions(models.Model):
    option_text = models.TextField(null=False, blank=False)
    is_correct = models.BooleanField(default=False, null=False)
    option_num = models.PositiveIntegerField(null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.option_text


class BaseExplanations(models.Model):
    explanation_text = models.TextField(blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.explanation_text


class PYQuestions(models.Model):
    subject = models.CharField(max_length=4, choices=[(code.value, code.name) for code in cu.SubjectCode])
    question_text = models.TextField(null=False, blank=False)
    year = models.PositiveIntegerField(null=False)
    q_num = models.PositiveIntegerField(null=False)
    explanation = models.OneToOneField('PYQExplanations', on_delete=models.CASCADE, related_name='question')

    class Meta:
        ordering = ['year', 'q_num']
        db_table = 'prelims_pyqs'
        unique_together = ('year', 'q_num')

    def __str__(self):
        return self.question_text[:50] + "..."


class PYQOptions(BaseOptions):
    question = models.ForeignKey('PYQuestions', on_delete=models.CASCADE, related_name='options')

    class Meta:
        ordering = ['option_num']
        db_table = 'prelims_pyq_options'
        unique_together = ('question', 'option_num')


class PYQExplanations(BaseExplanations):
    class Meta:
        db_table = 'prelims_pyq_explanations'


class BaseMockMCQ(models.Model):
    question_text = models.TextField(null=False, blank=False)
    pattern_type = models.CharField(max_length=15, choices=[(pattern_type.value, pattern_type.name) for pattern_type in
                                                            cu.PatternType])
    difficulty_level = models.CharField(max_length=10,
                                        choices=[(difficulty_level.value, difficulty_level.name) for difficulty_level in
                                                 cu.QuestionDifficultyLevel])
    explanation = models.OneToOneField('MockMCQExplanations', on_delete=models.CASCADE, related_name='%(class)s')

    class Meta:
        abstract = True

    def __str__(self):
        return self.question_text[:50] + "..."


class HistoryMockMCQ(BaseMockMCQ):
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
        db_table = 'prelims_mock_economics'


class ScienceAndTechMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_science_and_tech'


class EnvironmentMockMCQ(BaseMockMCQ):
    class Meta:
        db_table = 'prelims_mock_mcq_environment'


class CurrentAffairsMockMCQ(BaseMockMCQ):
    subject = models.CharField(max_length=4, choices=[(code.value, code.name) for code in cu.SubjectCode])

    class Meta:
        db_table = 'prelims_mock_mcq_current_affairs'


class MockMCQOptions(BaseOptions):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')


class MockMCQExplanations(BaseExplanations):
    class Meta:
        db_table = 'prelims_mock_mcq_answer_explanations'

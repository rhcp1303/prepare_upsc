from django.core.management.base import BaseCommand
from ...helpers import rag_langchain_helper as helper
import logging
from ...helpers import common_utils as cu

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, help='subject of mcq to be generated',
                            choices=[code.value for code in cu.SubjectCode],
                            required=True)
        parser.add_argument('--topic', type=str, help='topic of mcq to be generated', required=False)
        parser.add_argument('--pattern_type', type=int, help='pattern type of mcq to be generated',
                            choices=[pattern_type.value for pattern_type in cu.PatternType], required=True)

        parser.add_argument('--difficulty_level', type=str, help='difficulty level of mcq to be generated',
                            choices=[diff_level.value for diff_level in cu.QuestionDifficultyLevel],
                            required=True)

    def handle(self, *args, **options):
        subject = options['subject']
        topic = options['topic']
        pattern_type = options['pattern_type']
        difficulty_level = options['difficulty_level']
        logger.info(
            f"Starting generation of of question based on \nsubject: {subject}\ntopic: {topic}\npattern type: {pattern_type}\ndifficulty level: {difficulty_level}")
        helper.generate_mock_mcq(subject, topic, pattern_type, difficulty_level)

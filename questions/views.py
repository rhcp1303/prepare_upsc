from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MockMCQ, PYQuestions
from .serializers import MockMCQSerializer, PYQSerializer
from django.shortcuts import render
from . import services
from .helpers import query_question_helper as helper


@api_view(['GET'])
def get_subject_wise_mock_mcq(request):
    subject = request.GET.get('subject', None)
    num_questions = int(request.GET.get('num_questions', 20))
    if num_questions <= 0:
        return Response({"error": "Invalid number of questions"}, status=400)
    if subject:
        questions = MockMCQ.objects.filter(subject=subject).order_by('?')[:num_questions]
    else:
        questions = MockMCQ.objects.order_by('?')[:num_questions]
    serializer = MockMCQSerializer(questions, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def get_year_wise_pyq(request):
    year = request.GET.get('year', None)
    questions = PYQuestions.objects.filter(year=year).order_by('q_num')
    serializer = PYQSerializer(questions, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def get_comprehensive_mock_mcq(request):
    subject_quotas = {
        "MIH": {"STATIC": 10, "CA": 0},
        "HAC": {"STATIC": 4, "CA": 2},
        "POL": {"STATIC": 10, "CA": 7},
        "IRS": {"STATIC": 0, "CA": 4},
        "ECO": {"STATIC": 6, "CA": 9},
        "SNT": {"STATIC": 5, "CA": 9},
        "ENV": {"STATIC": 6, "CA": 10},
        "GEO": {"STATIC": 16, "CA": 0},
        "SOCI": {"STATIC": 0, "CA": 2}
    }
    subject_quotas = request.GET.get('subject_quotas', subject_quotas)
    questions = services.get_mock_mcq(subject_quotas)
    serializer = MockMCQSerializer(questions, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def evaluate_test(request):
    data = request.data
    questions = data.get('questions')
    answers = data.get('answers')
    score = 0
    explanations = []
    for i, question in enumerate(questions):
        correct_answer_index = question['correct_option']
        user_answer_index = answers.get(str(i))
        is_correct = user_answer_index is not None and user_answer_index == correct_answer_index
        if is_correct:
            score += 1
        explanations.append(question['explanation'])
    return Response({'score': score, 'explanations': explanations})


def subject_wise_mock_test_view(request):
    return render(request, 'subject_wise_mock_test.html')


def demo2_view(request):
    return render(request, 'demo2.html')


def quiz_view(request):
    return render(request, 'quiz_view.html')


def pyq_view(request):
    return render(request, 'pyq_view.html')


@api_view(['GET'])
def get_quiz_questions(request):
    query = request.GET.get('query')
    num_questions = 100
    try:
        questions = helper.query_question(query, num_questions)
        return Response(questions, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

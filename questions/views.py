from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MockMCQ, PYQuestions
from .serializers import MockMCQSerializer, PYQSerializer
from django.shortcuts import render
from . import services
import json


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
def test1(request):
    with open('questions/data/flt/test1.json', 'r') as f:
        data = json.load(f)
    return Response(data, status=200)


@api_view(['GET'])
def get_comprehensive_mock_mcq(request):
    subject_quotas = {
        "MIH": {"STATIC": 10, "CA": 0},
        "HAC": {"STATIC": 4, "CA": 2},
        "POL": {"STATIC": 10, "CA": 11},
        "ECO": {"STATIC": 8, "CA": 9},
        "SNT": {"STATIC": 5, "CA": 9},
        "ENV": {"STATIC": 6, "CA": 10},
        "GEO": {"STATIC": 10, "CA": 6},
    }
    subject_quotas = request.GET.get('subject_quotas', subject_quotas)
    questions = services.get_mock_mcq(subject_quotas)

    serializer = MockMCQSerializer(questions, many=True)
    with open("temp/test2.json", "w") as f:
        f.write(json.dumps(serializer.data))
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


def test1_view(request):
    return render(request, 'test1_view.html')

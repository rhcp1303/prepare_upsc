from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MockMCQ
from .serializers import MockMCQSerializer
from django.shortcuts import render

@api_view(['GET'])
def get_mock_mcq(request):
    subject = request.GET.get('subject', None)
    num_questions = int(request.GET.get('num_questions', 20))
    if num_questions <= 0:
        return Response({"error": "Invalid number of questions"}, status=400)
    if subject:
        questions = MockMCQ.objects.filter(subject=subject).order_by('?')[:num_questions]
    else:
        questions = MockMCQ.objects.order_by('?')[:num_questions]
    serializer = MockMCQSerializer(questions, many=True)
    return Response({"questions": serializer.data}, status=200)


def mock_test_view(request):
    return render(request, 'index.html')


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

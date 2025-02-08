from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MockMCQ
from .serializers import MockMCQSerializer


@api_view(['GET'])
def generate_mock_test(request):
    subject = request.GET.get('subject', None)
    num_questions = int(request.GET.get('num_questions', 50))
    if num_questions <= 0:
        return Response({"error": "Invalid number of questions"}, status=400)
    if subject:
        questions = MockMCQ.objects.filter(subject=subject).order_by('?')[:num_questions]
    else:
        questions = MockMCQ.objects.order_by('?')[:num_questions]
    serializer = MockMCQSerializer(questions, many=True)
    return Response({"questions": serializer.data}, status=200)

from rest_framework import serializers
from .models import MockMCQ,PYQuestions


class MockMCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockMCQ
        fields = '__all__'

class PYQSerializer(serializers.ModelSerializer):
    class Meta:
        model = PYQuestions
        fields = '__all__'
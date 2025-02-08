from rest_framework import serializers
from .models import MockMCQ


class MockMCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockMCQ
        fields = '__all__'
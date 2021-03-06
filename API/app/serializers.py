from app.models import Test
from rest_framework import serializers

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('machine', 'value')

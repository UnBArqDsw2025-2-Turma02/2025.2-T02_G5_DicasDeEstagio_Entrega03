from rest_framework import serializers
from .models import Curriculo

class CurriculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculo
        fields = '__all__'
        
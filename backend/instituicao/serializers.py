from rest_framework import serializers
from .models import Instituicao

class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = '__all__'
        
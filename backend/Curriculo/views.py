from django.shortcuts import render
from rest_framework import viewsets
from .models import Curriculo 
from .serializers import CurriculoSerializer

class CurriculoViewSet(viewsets.ModelViewSet):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer
    

from django import forms
from .models import Empresa

class AvaliacaoForm(forms.Form):
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all())
    nota_geral = forms.IntegerField(min_value=1, max_value=5)
    
    titulo = forms.CharField(max_length=200)
    pros = forms.CharField(widget=forms.Textarea)
    contras = forms.CharField(widget=forms.Textarea)
    
    cargo = forms.CharField(max_length=100)
    anonima = forms.BooleanField(required=False)
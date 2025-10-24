from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nota_geral = models.PositiveSmallIntegerField() 

    titulo = models.CharField(max_length=200, blank=True, null=True)
    pros = models.TextField(blank=True, null=True)
    contras = models.TextField(blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    anonima = models.BooleanField(default=False)
    
    criada_em = models.DateTimeField(auto_now_add=True)

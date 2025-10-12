from django.db import models

class Instituicao(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)
    AreaAtuacao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
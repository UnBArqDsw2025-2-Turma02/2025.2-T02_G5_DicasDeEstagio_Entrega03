from django.db import models
from users.models import User

class Curriculo(models.Model):
    competencias = models.TextField()
    arquivo = models.FileField(upload_to='curriculos/')
    formacao = models.TextField()
    habilidade = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'Currículo de {self.user.email}'

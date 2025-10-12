from django.db import models

class Avaliacao(models.Model):
    nota = [ 
        (1, 'Muito Ruim'),
        (2, 'Ruim'),
        (3, 'Regular'),
        (4, 'Bom'),
        (5, 'Muito Bom'),
    ]
    
    nota = models.IntegerField(choices=nota)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    datainicio = models.DateTimeField()
    datafim = models.DateTimeField()
    comentario = models.TextField()

    def __str__(self):
        return f'Avaliação {self.nota} - {self.datainicio.strftime("%Y-%m-%d %H:%M:%S")}'
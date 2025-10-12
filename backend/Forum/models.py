from django.db import models
from django.conf import settings


class Forum(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topicos_forum')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    visualizacoes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Tópico do Fórum'
        verbose_name_plural = 'Tópicos do Fórum'

    def __str__(self):
        return self.titulo

    @property
    def total_comentarios(self):
        return self.comentarios.filter(is_active=True).count()


class ComentarioForum(models.Model):
    topico = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios_forum')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    comentario_pai = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='respostas'
    )

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        if self.comentario_pai:
            return f'Resposta de {self.user.email} para comentário em "{self.topico.titulo}"'
        return f'Comentário de {self.user.email} em "{self.topico.titulo}"'

    @property
    def total_respostas(self):
        return self.respostas.filter(is_active=True).count()

    def is_resposta(self):
        return self.comentario_pai is not None
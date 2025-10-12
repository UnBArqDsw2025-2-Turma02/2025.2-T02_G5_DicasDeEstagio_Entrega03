from django.contrib import admin
from .models import Forum, ComentarioForum


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'user', 'data_criacao', 'visualizacoes', 'is_active']
    list_filter = ['is_active', 'data_criacao']
    search_fields = ['titulo', 'conteudo', 'user__email']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'visualizacoes']
    date_hierarchy = 'data_criacao'


@admin.register(ComentarioForum)
class ComentarioForumAdmin(admin.ModelAdmin):
    list_display = ['get_short_content', 'user', 'topico', 'comentario_pai', 'data_criacao', 'is_active']
    list_filter = ['is_active', 'data_criacao']
    search_fields = ['conteudo', 'user__email', 'topico__titulo']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    date_hierarchy = 'data_criacao'
    
    def get_short_content(self, obj):
        return obj.conteudo[:50] + '...' if len(obj.conteudo) > 50 else obj.conteudo
    get_short_content.short_description = 'Conteúdo'

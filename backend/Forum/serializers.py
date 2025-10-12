from rest_framework import serializers
from .models import Forum, ComentarioForum


class ComentarioForumSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    total_respostas = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ComentarioForum
        fields = [
            'id', 'topico', 'user', 'user_email', 'user_name', 
            'conteudo', 'data_criacao', 'data_atualizacao', 
            'is_active', 'comentario_pai', 'total_respostas'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao', 'user']


class ForumSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    total_comentarios = serializers.IntegerField(read_only=True)
    comentarios = ComentarioForumSerializer(many=True, read_only=True)
    
    class Meta:
        model = Forum
        fields = [
            'id', 'titulo', 'conteudo', 'user', 'user_email', 'user_name',
            'data_criacao', 'data_atualizacao', 'visualizacoes', 
            'is_active', 'total_comentarios', 'comentarios'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao', 'user', 'visualizacoes']


class ForumListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de tópicos (sem comentários)"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    total_comentarios = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Forum
        fields = [
            'id', 'titulo', 'conteudo', 'user', 'user_email', 'user_name',
            'data_criacao', 'data_atualizacao', 'visualizacoes', 
            'is_active', 'total_comentarios'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao', 'user', 'visualizacoes']

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Forum, ComentarioForum
from .serializers import ForumSerializer, ForumListSerializer, ComentarioForumSerializer


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ForumListSerializer
        return ForumSerializer
    
    def perform_create(self, serializer):
        """Define o usuário atual ao criar um tópico"""
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visualizacoes += 1
        instance.save(update_fields=['visualizacoes'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comentarios(self, request, pk=None):
        topico = self.get_object()
        comentarios = topico.comentarios.filter(is_active=True, comentario_pai=None)
        serializer = ComentarioForumSerializer(comentarios, many=True)
        return Response(serializer.data)


class ComentarioForumViewSet(viewsets.ModelViewSet):
    queryset = ComentarioForum.objects.all()
    serializer_class = ComentarioForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Define o usuário atual ao criar um comentário"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def respostas(self, request, pk=None):
        comentario = self.get_object()
        respostas = comentario.respostas.filter(is_active=True)
        serializer = self.get_serializer(respostas, many=True)
        return Response(serializer.data)


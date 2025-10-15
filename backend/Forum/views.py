from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Forum, ComentarioForum
from .serializers import ForumSerializer, ForumListSerializer, ComentarioForumSerializer
from core.decorators import log_request  


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ForumListSerializer
        return ForumSerializer
    
    @log_request  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @log_request  
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @log_request  
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visualizacoes += 1
        instance.save(update_fields=['visualizacoes'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @log_request  
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @log_request  
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    @log_request 
    def comentarios(self, request, pk=None):
        topico = self.get_object()
        comentarios = topico.comentarios.filter(is_active=True, comentario_pai=None)
        serializer = ComentarioForumSerializer(comentarios, many=True)
        return Response(serializer.data)


class ComentarioForumViewSet(viewsets.ModelViewSet):

    queryset = ComentarioForum.objects.all()
    serializer_class = ComentarioForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @log_request  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @log_request  
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @log_request  
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    @log_request 
    def respostas(self, request, pk=None):
        comentario = self.get_object()
        respostas = comentario.respostas.filter(is_active=True)
        serializer = self.get_serializer(respostas, many=True)
        return Response(serializer.data)


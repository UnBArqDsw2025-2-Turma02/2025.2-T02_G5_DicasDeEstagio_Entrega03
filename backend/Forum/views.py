from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Forum, ComentarioForum
from .serializers import ForumSerializer, ForumListSerializer, ComentarioForumSerializer
from .factories.topico_factory import TopicoFactory


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
    
    @action(detail=False, methods=['post'], url_path='criar-por-tipo')
    def criar_topico_por_tipo(self, request):
        """
        Endpoint para criar tópicos usando o Factory Method
        
        Exemplos de payload:
        
        VAGA:
        {
            "tipo_topico": "vaga",
            "titulo": "Desenvolvedor Python",
            "conteudo": "Vaga para desenvolvedor...",
            "salario": "R$ 3.000",
            "requisitos": "Python, Django",
            "empresa": "Tech Corp",
            "tipo_vaga": "Estágio"
        }
        
        DÚVIDA:
        {
            "tipo_topico": "duvida",
            "titulo": "Como me preparar?",
            "conteudo": "Preciso de ajuda...",
            "categoria": "Entrevistas",
            "urgencia": "Alta",
            "tags": ["entrevista", "dicas"]
        }
        """
        try:
            # Extrair dados obrigatórios do request
            tipo_topico = request.data.get('tipo_topico')
            titulo = request.data.get('titulo')
            conteudo = request.data.get('conteudo')
            
            # Validações básicas
            if not all([tipo_topico, titulo, conteudo]):
                return Response(
                    {'error': 'Campos obrigatórios: tipo_topico, titulo, conteudo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar o Factory Method para criar o tópico
            topico = TopicoFactory.create_topico(
                tipo_topico=tipo_topico,
                user=request.user,
                titulo=titulo,
                conteudo=conteudo,
                **{k: v for k, v in request.data.items() 
                   if k not in ['tipo_topico', 'titulo', 'conteudo']}
            )
            
            # Serializar e retornar o tópico criado
            serializer = self.get_serializer(topico)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erro interno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='tipos-disponiveis')
    def tipos_disponiveis(self, request):
        """
        Endpoint para listar os tipos de tópicos disponíveis
        """
        tipos_info = TopicoFactory.get_tipos_disponiveis()
        
        return Response({
            'tipos_disponiveis': tipos_info,
            'total_tipos': len(tipos_info),
            'instrucoes': {
                'como_usar': 'Use o endpoint /criar-por-tipo/ com o tipo desejado',
                'campos_obrigatorios': ['tipo_topico', 'titulo', 'conteudo'],
                'exemplo_url': '/api/forum/criar-por-tipo/'
            }
        })
    
    @action(detail=False, methods=['get'], url_path='por-tipo/(?P<tipo>[^/.]+)')
    def listar_por_tipo(self, request, tipo=None):
        """
        Endpoint para listar tópicos por tipo
        URL: /api/forum/por-tipo/vaga/
        """
        if not tipo:
            return Response(
                {'error': 'Tipo de tópico não especificado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mapear tipos para marcadores nos títulos
        marcadores = {
            'vaga': '[VAGA',
            'duvida': '[DÚVIDA',
            'experiencia': '[EXPERIÊNCIA',
            'dica': '[DICA',
            'discussao': '[DISCUSSÃO'
        }
        
        marcador = marcadores.get(tipo.lower())
        if not marcador:
            return Response(
                {'error': f'Tipo inválido. Tipos disponíveis: {list(marcadores.keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar tópicos por tipo baseado no título
        topicos = self.queryset.filter(titulo__icontains=marcador).order_by('-data_criacao')
        
        # Aplicar paginação se necessário
        page = self.paginate_queryset(topicos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(topicos, many=True)
        
        return Response({
            'tipo': tipo,
            'total': topicos.count(),
            'topicos': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='estatisticas-tipos')
    def estatisticas_tipos(self, request):
        """
        Endpoint para ver estatísticas dos tipos de tópicos
        """
        marcadores = {
            'vaga': '[VAGA',
            'duvida': '[DÚVIDA',
            'experiencia': '[EXPERIÊNCIA',
            'dica': '[DICA',
            'discussao': '[DISCUSSÃO'
        }
        
        estatisticas = {}
        total_geral = 0
        
        for tipo, marcador in marcadores.items():
            count = self.queryset.filter(titulo__icontains=marcador).count()
            estatisticas[tipo] = {
                'total': count,
                'ativo': self.queryset.filter(
                    titulo__icontains=marcador, 
                    is_active=True
                ).count(),
                'com_comentarios': self.queryset.filter(
                    titulo__icontains=marcador
                ).exclude(comentarios__isnull=True).distinct().count()
            }
            total_geral += count
        
        # Contar tópicos sem tipo específico
        topicos_sem_tipo = self.queryset.exclude(
            titulo__iregex=r'\[(VAGA|DÚVIDA|EXPERIÊNCIA|DICA|DISCUSSÃO)'
        ).count()
        
        estatisticas['outros'] = {
            'total': topicos_sem_tipo,
            'ativo': self.queryset.filter(is_active=True).exclude(
                titulo__iregex=r'\[(VAGA|DÚVIDA|EXPERIÊNCIA|DICA|DISCUSSÃO)'
            ).count(),
            'com_comentarios': self.queryset.exclude(
                titulo__iregex=r'\[(VAGA|DÚVIDA|EXPERIÊNCIA|DICA|DISCUSSÃO)'
            ).exclude(comentarios__isnull=True).distinct().count()
        }
        
        total_geral += topicos_sem_tipo
        
        return Response({
            'estatisticas_por_tipo': estatisticas,
            'total_geral': total_geral,
            'total_tipos_implementados': len(marcadores),
            'data_consulta': request.META.get('HTTP_DATE', 'N/A')
        })


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


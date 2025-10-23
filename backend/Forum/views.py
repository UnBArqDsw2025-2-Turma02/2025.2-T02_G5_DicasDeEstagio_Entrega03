from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Forum, ComentarioForum
from .serializers import ForumSerializer, ForumListSerializer, ComentarioForumSerializer
from .factories.topico_factory import TopicoFactory
from .iterators.forum_iterators import ForumCollection
from rest_framework.decorators import action
from core.decorators import log_request
import logging
import time

logger = logging.getLogger(__name__)

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ForumListSerializer
        return ForumSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visualizacoes += 1
        instance.save(update_fields=['visualizacoes'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def comentarios(self, request, pk=None):
        topico = self.get_object()
        comentarios = topico.comentarios.filter(is_active=True, comentario_pai=None)
        serializer = ComentarioForumSerializer(comentarios, many=True)
        return Response(serializer.data)
    
    def criar_topico_por_tipo(self, request):
        if not request.user.is_authenticated:
            return Response(
                {
                    'error': 'Autenticação necessária',
                    'detail': 'Você precisa estar autenticado para criar tópicos',
                    'dica': 'Use o endpoint /api/auth/register/ para criar uma conta'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        tipo_topico = request.data.get('tipo_topico')
        titulo = request.data.get('titulo')
        conteudo = request.data.get('conteudo')
        
        if not all([tipo_topico, titulo, conteudo]):
            return Response(
                {'error': 'Campos obrigatórios: tipo_topico, titulo, conteudo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        topico = TopicoFactory.create_topico(
            tipo_topico=tipo_topico,
            user=request.user,
            titulo=titulo,
            conteudo=conteudo,
            **{k: v for k, v in request.data.items() 
               if k not in ['tipo_topico', 'titulo', 'conteudo']}
        )
        
        serializer = self.get_serializer(topico)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def tipos_disponiveis(self, request):
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
    
    def listar_por_tipo(self, request, tipo=None):
        if not tipo:
            return Response(
                {'error': 'Tipo de tópico não especificado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
        
        topicos = self.queryset.filter(titulo__icontains=marcador).order_by('-data_criacao')
        
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
    
    def estatisticas_tipos(self, request):
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
    
    def listar_por_tipo_iterator(self, request, tipo=None):
        if not tipo:
            return Response(
                {'error': 'Tipo de tópico é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            collection = ForumCollection(self.queryset)
            iterator = collection.create_iterator_por_tipo(tipo)
            
            topicos = []
            while iterator.has_next():
                topico = iterator.next()
                topicos.append({
                    'id': topico.id,
                    'titulo': topico.titulo,
                    'conteudo': topico.conteudo[:200] + '...' if len(topico.conteudo) > 200 else topico.conteudo,
                    'user': topico.user.email,
                    'data_criacao': topico.data_criacao,
                    'visualizacoes': topico.visualizacoes
                })
            
            return Response({
                'tipo_topico': tipo,
                'total_encontrado': iterator.get_total(),
                'topicos': topicos,
                'implementacao': {
                    'padrao_usado': 'Iterator Pattern (Versão Mínima)',
                    'iterator_type': 'TopicoPorTipoIterator',
                    'integrado_com': 'Factory Method Pattern',
                    'demonstra': 'Navegação eficiente por tipo específico'
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def demonstracao_iterator_minimo(self, request):
        try:
            tipos_factory = TopicoFactory.get_tipos_disponiveis()
            
            collection = ForumCollection(self.queryset)
            estatisticas_iterator = {}
            
            for tipo in tipos_factory.keys():
                iterator = collection.create_iterator_por_tipo(tipo)
                total = iterator.get_total()
                
                estatisticas_iterator[tipo] = {
                    'total': total,
                    'exemplo_titulo': None
                }
                
                if iterator.has_next():
                    exemplo = iterator.next()
                    estatisticas_iterator[tipo]['exemplo_titulo'] = exemplo.titulo
            
            return Response({
                'versao': 'Iterator Pattern - Implementação Mínima',
                'objetivo': 'Demonstrar integração essencial entre Factory Method e Iterator',
                'factory_method': {
                    'funcao': 'Cria tópicos com formatação padronizada',
                    'tipos_disponiveis': list(tipos_factory.keys()),
                    'exemplo_uso': 'TopicoFactory.create_topico(tipo, user, titulo, conteudo)'
                },
                'iterator_pattern': {
                    'funcao': 'Navega através de tópicos filtrados por tipo',
                    'implementacao': 'TopicoPorTipoIterator',
                    'exemplo_uso': 'ForumCollection().create_iterator_por_tipo(tipo)'
                },
                'integracao': {
                    'workflow': [
                        '1. Factory Method cria tópicos com marcadores ([VAGA], [DÚVIDA], etc.)',
                        '2. Iterator filtra automaticamente pelos marcadores',
                        '3. Navegação eficiente sem expor estrutura interna'
                    ],
                    'beneficios': [
                        'Baixo acoplamento entre componentes',
                        'Separação clara de responsabilidades',
                        'Facilidade de manutenção e extensão'
                    ]
                },
                'estatisticas_atuais': estatisticas_iterator,
                'endpoint_teste': '/api/forum/iterator-por-tipo/{tipo}/'
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro na demonstração: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ComentarioForumViewSet(viewsets.ModelViewSet):
    queryset = ComentarioForum.objects.all()
    serializer_class = ComentarioForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def respostas(self, request, pk=None):
        comentario = self.get_object()
        respostas = comentario.respostas.filter(is_active=True)
        serializer = self.get_serializer(respostas, many=True)
        return Response(serializer.data)
    
    def navegar_por_tipo_iterator(self, request, tipo=None):
        """
        Endpoint que usa o padrão Iterator para navegar por tópicos de um tipo específico
        Demonstra a integração entre Factory Method e Iterator
        
        URL: /api/forum/navegar-por-tipo/vaga/
        """
        if not tipo:
            return Response(
                {'error': 'Tipo de tópico é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Criar coleção de tópicos usando o padrão Iterator
            forum_collection = ForumCollection(self.queryset)
            iterator = forum_collection.create_iterator_por_tipo(tipo)
            
            # Parâmetros de paginação
            page = int(request.query_params.get('page', 1))
            per_page = int(request.query_params.get('per_page', 10))
            
            # Calcular posições
            start_position = (page - 1) * per_page
            
            # Resetar iterator e avançar até a posição inicial
            iterator.reset()
            for _ in range(start_position):
                if not iterator.has_next():
                    break
                iterator.next()
            
            # Coletar itens da página atual
            topicos_pagina = []
            items_coletados = 0
            
            while iterator.has_next() and items_coletados < per_page:
                topico = iterator.next()
                topicos_pagina.append({
                    'id': topico.id,
                    'titulo': topico.titulo,
                    'conteudo': topico.conteudo[:200] + '...' if len(topico.conteudo) > 200 else topico.conteudo,
                    'user': topico.user.email,
                    'data_criacao': topico.data_criacao,
                    'visualizacoes': topico.visualizacoes,
                    'total_comentarios': topico.total_comentarios,
                    'is_active': topico.is_active
                })
                items_coletados += 1
            
            # Calcular informações de paginação
            total_items = iterator.get_total()
            total_pages = (total_items + per_page - 1) // per_page
            
            return Response({
                'tipo_topico': tipo,
                'topicos': topicos_pagina,
                'paginacao': {
                    'pagina_atual': page,
                    'por_pagina': per_page,
                    'total_paginas': total_pages,
                    'total_items': total_items,
                    'tem_proxima': page < total_pages,
                    'tem_anterior': page > 1
                },
                'metadados': {
                    'padrao_usado': 'Iterator Pattern',
                    'tipo_iterator': 'TopicoPorTipoIterator',
                    'integrado_com': 'Factory Method Pattern'
                }
            })
            
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
    
    def comentarios_arvore_iterator(self, request, pk=None):
        """
        Endpoint que usa Iterator para navegar através da árvore de comentários
        Implementa travessia em profundidade (DFS)
        
        URL: /api/forum/{id}/comentarios-arvore/
        """
        try:
            topico = self.get_object()
            incluir_inativos = request.query_params.get('incluir_inativos', 'false').lower() == 'true'
            
            # Criar iterator para comentários em árvore
            iterator_comentarios = ComentarioArvoreIterator(topico, incluir_inativos)
            
            # Estruturar comentários com informações de hierarquia
            comentarios_estruturados = []
            nivel_map = {}  # Mapear comentário -> nível na árvore
            
            while iterator_comentarios.has_next():
                comentario = iterator_comentarios.next()
                
                # Calcular nível na árvore
                if comentario.comentario_pai is None:
                    nivel = 0
                else:
                    nivel = nivel_map.get(comentario.comentario_pai.id, 0) + 1
                
                nivel_map[comentario.id] = nivel
                
                comentarios_estruturados.append({
                    'id': comentario.id,
                    'conteudo': comentario.conteudo,
                    'user': comentario.user.email,
                    'data_criacao': comentario.data_criacao,
                    'data_atualizacao': comentario.data_atualizacao,
                    'is_active': comentario.is_active,
                    'comentario_pai_id': comentario.comentario_pai.id if comentario.comentario_pai else None,
                    'nivel_hierarquia': nivel,
                    'total_respostas': comentario.total_respostas,
                    'e_resposta': comentario.is_resposta()
                })
            
            return Response({
                'topico': {
                    'id': topico.id,
                    'titulo': topico.titulo,
                    'total_comentarios': topico.total_comentarios
                },
                'comentarios': comentarios_estruturados,
                'estatisticas': {
                    'total_visitados': iterator_comentarios.get_visited_count(),
                    'niveis_profundidade': max(nivel_map.values()) + 1 if nivel_map else 0,
                    'comentarios_raiz': len([c for c in comentarios_estruturados if c['nivel_hierarquia'] == 0]),
                    'comentarios_resposta': len([c for c in comentarios_estruturados if c['e_resposta']])
                },
                'metadados': {
                    'padrao_usado': 'Iterator Pattern',
                    'tipo_iterator': 'ComentarioArvoreIterator (DFS)',
                    'algoritmo_travessia': 'Depth-First Search',
                    'incluiu_inativos': incluir_inativos
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro ao processar comentários: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def topicos_paginado_iterator(self, request):
        """
        Endpoint que demonstra Iterator Paginado para grandes volumes de dados        URL: /api/forum/paginado-avancado/
        """
        try:
            # Parâmetros de consulta
            page_size = int(request.query_params.get('page_size', 10))
            filtro_ativo = request.query_params.get('ativo', 'true').lower() == 'true'
            ordenacao = request.query_params.get('ordem', 'recente')  # recente, antigo, visualizacoes
            
            # Aplicar filtros ao queryset
            queryset = self.queryset
            if filtro_ativo:
                queryset = queryset.filter(is_active=True)
            
            # Aplicar ordenação
            if ordenacao == 'recente':
                queryset = queryset.order_by('-data_criacao')
            elif ordenacao == 'antigo':
                queryset = queryset.order_by('data_criacao')
            elif ordenacao == 'visualizacoes':
                queryset = queryset.order_by('-visualizacoes')
            
            # Criar coleção e iterator paginado
            forum_collection = ForumCollection(queryset)
            iterator_paginado = forum_collection.create_iterator_paginado(page_size)
            
            # Coletar todos os itens (ou até um limite para demonstração)
            limite_items = int(request.query_params.get('limite', 50))
            topicos_coletados = []
            items_processados = 0
            
            while iterator_paginado.has_next() and items_processados < limite_items:
                topico = iterator_paginado.next()
                topicos_coletados.append({
                    'id': topico.id,
                    'titulo': topico.titulo,
                    'user': topico.user.email,
                    'data_criacao': topico.data_criacao,
                    'visualizacoes': topico.visualizacoes,
                    'total_comentarios': topico.total_comentarios,
                    'pagina': iterator_paginado.get_current_page()
                })
                items_processados += 1
            
            return Response({
                'topicos': topicos_coletados,
                'configuracao': {
                    'page_size': page_size,
                    'filtro_ativo': filtro_ativo,
                    'ordenacao': ordenacao,
                    'limite_aplicado': limite_items
                },
                'estatisticas_paginacao': {
                    'total_items': iterator_paginado.get_total_items(),
                    'total_pages': iterator_paginado.get_total_pages(),
                    'pagina_atual': iterator_paginado.get_current_page(),
                    'items_coletados': len(topicos_coletados)
                },
                'metadados': {
                    'padrao_usado': 'Iterator Pattern',
                    'tipo_iterator': 'TopicoPaginadoIterator',
                    'beneficio': 'Carregamento eficiente de grandes volumes'
                }
            })
            
        except ValueError as e:
            return Response(
                {'error': f'Parâmetro inválido: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erro interno: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def demonstracao_padroes(self, request):
        """
        Endpoint que demonstra a integração entre Factory Method e Iterator
        Mostra como os dois padrões trabalham juntos
        """
        try:
            # 1. Mostrar tipos disponíveis do Factory Method
            tipos_factory = TopicoFactory.get_tipos_disponiveis()
            
            # 2. Usar Iterator para contar tópicos por tipo
            forum_collection = ForumCollection(self.queryset.filter(is_active=True))
            estatisticas_iterator = {}
            
            for tipo in tipos_factory.keys():
                iterator = forum_collection.create_iterator_por_tipo(tipo)
                estatisticas_iterator[tipo] = {
                    'total': iterator.get_total(),
                    'exemplo_titulo': None
                }
                
                # Pegar um exemplo se existir
                if iterator.has_next():
                    exemplo = iterator.next()
                    estatisticas_iterator[tipo]['exemplo_titulo'] = exemplo.titulo
            
            # 3. Demonstrar criação + navegação (conceitual)
            return Response({
                'demonstracao': {
                    'factory_method': {
                        'descricao': 'Cria diferentes tipos de tópicos de forma padronizada',
                        'tipos_disponiveis': tipos_factory,
                        'uso': 'TopicoFactory.create_topico(tipo, user, titulo, conteudo, **kwargs)'
                    },
                    'iterator_pattern': {
                        'descricao': 'Navega através de coleções sem expor estrutura interna',
                        'tipos_implementados': [
                            'TopicoPorTipoIterator',
                            'ComentarioArvoreIterator', 
                            'TopicoPaginadoIterator'
                        ],
                        'uso': 'ForumCollection().create_iterator_por_tipo(tipo)'
                    }
                },
                'estatisticas_por_tipo': estatisticas_iterator,
                'integracao': {
                    'workflow': [
                        '1. Factory Method cria tópicos com formatação padronizada',
                        '2. Iterator navega pelos tópicos criados de forma eficiente',
                        '3. Ambos padrões mantêm baixo acoplamento e alta coesão'
                    ],
                    'beneficios': [
                        'Separação de responsabilidades',
                        'Facilidade de manutenção',
                        'Extensibilidade para novos tipos',
                        'Navegação eficiente em grandes volumes'
                    ]
                },
                'endpoints_demonstracao': {
                    'criar_topico_factory': '/api/forum/criar-por-tipo/',
                    'navegar_iterator': '/api/forum/navegar-por-tipo/{tipo}/',
                    'comentarios_arvore': '/api/forum/{id}/comentarios-arvore/',
                    'paginacao_avancada': '/api/forum/paginado-avancado/'
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erro na demonstração: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


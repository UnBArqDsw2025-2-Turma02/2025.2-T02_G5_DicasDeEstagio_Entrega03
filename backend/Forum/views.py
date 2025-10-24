from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from .models import Forum, ComentarioForum
from .serializers import ForumSerializer, ForumListSerializer, ComentarioForumSerializer
from .factories.topico_factory import TopicoFactory
from .iterators.forum_iterators import ForumCollection, TopicoPorTipoIterator

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
   
        if not tipo:
            return Response(
                {'error': 'Tipo de tópico é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Criar coleção de tópicos usando o padrão Iterator (usar Forum.objects, não self.queryset)
            forum_collection = ForumCollection(Forum.objects.all())
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
        Endpoint simplificado para listar comentários de um tópico
        URL: /api/forum/topicos/{id}/comentarios-arvore/
        """
        try:
            # Buscar o tópico
            topico = Forum.objects.get(pk=pk)
            incluir_inativos = request.query_params.get('incluir_inativos', 'false').lower() == 'true'
            
            # Buscar comentários
            if incluir_inativos:
                comentarios = topico.comentarios.all()
            else:
                comentarios = topico.comentarios.filter(is_active=True)
            
            # Estruturar comentários
            comentarios_estruturados = []
            nivel_map = {}
            
            for comentario in comentarios:
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
                    'total_visitados': len(comentarios_estruturados),
                    'niveis_profundidade': max(nivel_map.values()) + 1 if nivel_map else 0,
                    'comentarios_raiz': len([c for c in comentarios_estruturados if c['nivel_hierarquia'] == 0]),
                    'comentarios_resposta': len([c for c in comentarios_estruturados if c['e_resposta']])
                },
                'metadados': {
                    'incluiu_inativos': incluir_inativos
                }
            })
            
        except Forum.DoesNotExist:
            return Response(
                {'error': 'Tópico não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao processar comentários: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def topicos_paginado_iterator(self, request):
        """
        Endpoint que demonstra Iterator Pattern com filtros e ordenação
        URL: /api/forum/paginado-avancado/
        """
        try:
            # Parâmetros de consulta
            filtro_ativo = request.query_params.get('ativo', 'true').lower() == 'true'
            ordenacao = request.query_params.get('ordem', 'recente')  # recente, antigo, visualizacoes
            tipo_filtro = request.query_params.get('tipo', None)  # vaga, duvida, dica, etc.
            
            # Aplicar filtros ao queryset (usar Forum.objects, não self.queryset que é ComentarioForum)
            queryset = Forum.objects.all()
            if filtro_ativo:
                queryset = queryset.filter(is_active=True)
            
            # Aplicar ordenação
            if ordenacao == 'recente':
                queryset = queryset.order_by('-data_criacao')
            elif ordenacao == 'antigo':
                queryset = queryset.order_by('data_criacao')
            elif ordenacao == 'visualizacoes':
                queryset = queryset.order_by('-visualizacoes')
            
            # Criar coleção e iterator
            forum_collection = ForumCollection(queryset)
            
            # Se especificou tipo, usar iterator filtrado
            if tipo_filtro:
                iterator = forum_collection.create_iterator_por_tipo(tipo_filtro)
            else:
                # Iterator sem filtro de tipo (todos os tópicos)
                iterator = TopicoPorTipoIterator(queryset)
            
            # Coletar todos os itens
            topicos_coletados = []
            
            while iterator.has_next():
                topico = iterator.next()
                topicos_coletados.append({
                    'id': topico.id,
                    'titulo': topico.titulo,
                    'user': topico.user.email,
                    'data_criacao': topico.data_criacao,
                    'visualizacoes': topico.visualizacoes,
                    'total_comentarios': topico.total_comentarios,
                    'is_active': topico.is_active
                })
            
            return Response({
                'topicos': topicos_coletados,
                'configuracao': {
                    'filtro_ativo': filtro_ativo,
                    'ordenacao': ordenacao,
                    'tipo_filtro': tipo_filtro or 'todos'
                },
                'estatisticas': {
                    'total_items': iterator.get_total(),
                    'items_retornados': len(topicos_coletados)
                },
                'metadados': {
                    'padrao_usado': 'Iterator Pattern',
                    'tipo_iterator': 'TopicoPorTipoIterator',
                    'beneficio': 'Navegação eficiente com filtros customizados'
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
            
            # 2. Usar Iterator para contar tópicos por tipo (usar Forum.objects, não self.queryset)
            forum_collection = ForumCollection(Forum.objects.filter(is_active=True))
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


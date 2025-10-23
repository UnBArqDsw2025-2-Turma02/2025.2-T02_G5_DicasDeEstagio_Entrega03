from django.urls import path
from rest_framework import routers
from .views import ForumViewSet, ComentarioForumViewSet

app_name = 'forum'

router = routers.DefaultRouter()
router.register(r'topicos', ForumViewSet, basename='topico')
router.register(r'comentarios', ComentarioForumViewSet, basename='comentario')

urlpatterns = router.urls + [
    # Endpoints customizados do ForumViewSet
    path('criar-por-tipo/', 
         ForumViewSet.as_view({'post': 'criar_topico_por_tipo'}), 
         name='criar-por-tipo'),
    
    path('tipos-disponiveis/', 
         ForumViewSet.as_view({'get': 'tipos_disponiveis'}), 
         name='tipos-disponiveis'),
    
    path('por-tipo/<str:tipo>/', 
         ForumViewSet.as_view({'get': 'listar_por_tipo'}), 
         name='por-tipo'),
    
    path('estatisticas-tipos/', 
         ForumViewSet.as_view({'get': 'estatisticas_tipos'}), 
         name='estatisticas-tipos'),
    
    path('iterator-por-tipo/<str:tipo>/', 
         ForumViewSet.as_view({'get': 'listar_por_tipo_iterator'}), 
         name='iterator-por-tipo'),
    
    path('demonstracao-minima/', 
         ForumViewSet.as_view({'get': 'demonstracao_iterator_minimo'}), 
         name='demonstracao-minima'),
    
    path('topicos/<int:pk>/comentarios/', 
         ForumViewSet.as_view({'get': 'comentarios'}), 
         name='topico-comentarios'),
    
    # Endpoints do ComentarioForumViewSet
    path('comentarios/<int:pk>/respostas/', 
         ComentarioForumViewSet.as_view({'get': 'respostas'}), 
         name='comentario-respostas'),
    
    path('navegar-por-tipo/<str:tipo>/', 
         ComentarioForumViewSet.as_view({'get': 'navegar_por_tipo_iterator'}), 
         name='navegar-por-tipo'),
    
    path('topicos/<int:pk>/comentarios-arvore/', 
         ComentarioForumViewSet.as_view({'get': 'comentarios_arvore_iterator'}), 
         name='comentarios-arvore'),
    
    path('paginado-avancado/', 
         ComentarioForumViewSet.as_view({'get': 'topicos_paginado_iterator'}), 
         name='paginado-avancado'),
    
    path('demonstracao-padroes/', 
         ComentarioForumViewSet.as_view({'get': 'demonstracao_padroes'}), 
         name='demonstracao-padroes'),
]

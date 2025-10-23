from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.decorators import log_request
from Forum.models import Forum
from Forum.serializers import ForumSerializer
from Forum.factories.topico_factory import TopicoFactory


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_request
def criar_topico_com_decorator(request):
    tipo_topico = request.data.get('tipo_topico')
    titulo = request.data.get('titulo')
    conteudo = request.data.get('conteudo')
    
    if not all([tipo_topico, titulo, conteudo]):
        return Response(
            {'error': 'Campos obrigatórios: tipo_topico, titulo, conteudo'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        topico = TopicoFactory.create_topico(
            tipo_topico=tipo_topico,
            user=request.user,
            titulo=titulo,
            conteudo=conteudo,
            **{k: v for k, v in request.data.items() 
               if k not in ['tipo_topico', 'titulo', 'conteudo']}
        )
        
        serializer = ForumSerializer(topico)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@log_request
def deletar_topico_com_decorator(request, pk):
    try:
        topico = Forum.objects.get(pk=pk, user=request.user)
        
        topico.is_active = False
        topico.save()
        
        return Response({
            'message': 'Tópico desativado com sucesso',
            'topico': {
                'id': topico.id,
                'titulo': topico.titulo,
                'is_active': topico.is_active
            }
        }, status=status.HTTP_200_OK)
        
    except Forum.DoesNotExist:
        return Response(
            {'error': 'Tópico não encontrado ou você não tem permissão para deletá-lo'},
            status=status.HTTP_404_NOT_FOUND
        )

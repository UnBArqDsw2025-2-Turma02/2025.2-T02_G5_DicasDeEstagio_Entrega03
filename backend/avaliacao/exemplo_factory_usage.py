"""
Exemplo de uso do Factory Method para Avaliações

Este arquivo demonstra como usar o padrão Factory Method
implementado para criar diferentes tipos de avaliações.
"""

from datetime import datetime, timedelta
from django.utils import timezone
from users.models import User
from instituicao.models import Instituicao
from .factories.avaliacao_factory import AvaliacaoFactory


def exemplo_uso_factory():
    """
    Exemplo prático de como usar o Factory Method para avaliações
    """
    
    # Simular um usuário estudante
    user = User.objects.filter(role='estudante').first()
    if not user:
        print("Erro: Nenhum usuário estudante encontrado")
        return
    
    # 1. CRIAR AVALIAÇÃO DE ESTÁGIO
    print("=== Criando Avaliação de Estágio ===")
    try:
        avaliacao_estagio = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='estagio',
            user=user,
            nota=4,
            comentario="Ótima experiência de estágio, aprendi muito sobre desenvolvimento web",
            data_inicio=timezone.now() - timedelta(days=120),
            data_fim=timezone.now() - timedelta(days=30)
        )
        print(f"✅ Avaliação de estágio criada: {avaliacao_estagio}")
    except Exception as e:
        print(f"❌ Erro ao criar avaliação de estágio: {e}")
    
    # 2. CRIAR AVALIAÇÃO DE EMPRESA
    print("\n=== Criando Avaliação de Empresa ===")
    try:
        # Buscar uma instituição para associar
        instituicao = Instituicao.objects.first()
        
        avaliacao_empresa = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='empresa',
            user=user,
            nota=5,
            comentario="Empresa excelente, ambiente colaborativo e oportunidades de crescimento",
            instituicao=instituicao
        )
        print(f"✅ Avaliação de empresa criada: {avaliacao_empresa}")
    except Exception as e:
        print(f"❌ Erro ao criar avaliação de empresa: {e}")
    
    # 3. CRIAR AVALIAÇÃO DE PROCESSO SELETIVO
    print("\n=== Criando Avaliação de Processo Seletivo ===")
    try:
        avaliacao_processo = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='processo_seletivo',
            user=user,
            nota=3,
            comentario="Processo seletivo demorado, mas bem estruturado",
            tipo_processo="Entrevista Técnica"
        )
        print(f"✅ Avaliação de processo seletivo criada: {avaliacao_processo}")
    except Exception as e:
        print(f"❌ Erro ao criar avaliação de processo seletivo: {e}")
    
    # 4. DEMONSTRAR TRATAMENTO DE ERRO
    print("\n=== Testando Tratamento de Erros ===")
    try:
        AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='tipo_inexistente',
            user=user,
            nota=3,
            comentario="Teste de erro"
        )
    except ValueError as e:
        print(f"✅ Erro capturado corretamente: {e}")
    
    # 5. USAR CREATORS DIRETAMENTE
    print("\n=== Usando Creators Diretamente ===")
    try:
        estagio_creator = AvaliacaoFactory.get_creator('estagio')
        avaliacao_direta = estagio_creator.create_avaliacao(
            user=user,
            nota=4,
            comentario="Usando creator diretamente"
        )
        print(f"✅ Avaliação criada diretamente: {avaliacao_direta}")
    except Exception as e:
        print(f"❌ Erro ao usar creator diretamente: {e}")


def listar_avaliacoes_por_tipo():
    """
    Lista as avaliações agrupadas por tipo
    """
    from avaliacao.models import Avaliacao
    
    print("\n=== Listando Avaliações por Tipo ===")
    
    avaliacoes = Avaliacao.objects.all()
    
    tipos = {
        'estagio': [],
        'empresa': [],
        'processo_seletivo': [],
        'outros': []
    }
    
    for avaliacao in avaliacoes:
        comentario = avaliacao.comentario.lower()
        if '[estágio]' in comentario or '[estagio]' in comentario:
            tipos['estagio'].append(avaliacao)
        elif '[empresa]' in comentario:
            tipos['empresa'].append(avaliacao)
        elif '[processo seletivo' in comentario:
            tipos['processo_seletivo'].append(avaliacao)
        else:
            tipos['outros'].append(avaliacao)
    
    for tipo, lista_avaliacoes in tipos.items():
        print(f"\n📊 {tipo.upper()}: {len(lista_avaliacoes)} avaliações")
        for avaliacao in lista_avaliacoes[:3]:  # Mostrar apenas as 3 primeiras
            print(f"  - Nota {avaliacao.nota}: {avaliacao.comentario[:50]}...")


if __name__ == "__main__":
    exemplo_uso_factory()
    listar_avaliacoes_por_tipo()

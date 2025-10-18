"""
Exemplo de uso do Factory Method para Tópicos do Fórum

Este arquivo demonstra como usar o padrão Factory Method
implementado para criar diferentes tipos de tópicos no fórum.
"""

from django.utils import timezone
from users.models import User
from instituicao.models import Instituicao
from Forum.factories.topico_factory import TopicoFactory


def exemplo_uso_topico_factory():
    """
    Exemplo prático de como usar o Factory Method para tópicos
    """
    
    # Simular um usuário
    user = User.objects.first()
    if not user:
        print("Erro: Nenhum usuário encontrado")
        return
    
    print(f"=== Criando tópicos como usuário: {user.email} ===\n")
    
    # 1. CRIAR TÓPICO DE VAGA
    print("1. 📢 Criando Tópico de Vaga...")
    try:
        topico_vaga = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=user,
            titulo='Desenvolvedor Python Júnior',
            conteudo='Estamos procurando um desenvolvedor Python para nossa equipe. '
                    'Experiência com Django é um diferencial.',
            salario='R$ 2.000,00 - R$ 3.000,00',
            requisitos='Python, Django, Git, conhecimento em bancos de dados',
            empresa='Tech Solutions Ltda',
            tipo_vaga='Estágio'
        )
        print(f"✅ Tópico de vaga criado: {topico_vaga.titulo}")
        print(f"   Conteúdo: {topico_vaga.conteudo[:100]}...")
    except Exception as e:
        print(f"❌ Erro ao criar tópico de vaga: {e}")
    
    # 2. CRIAR TÓPICO DE DÚVIDA
    print("\n2. ❓ Criando Tópico de Dúvida...")
    try:
        topico_duvida = TopicoFactory.create_topico(
            tipo_topico='duvida',
            user=user,
            titulo='Como me preparar para entrevista técnica?',
            conteudo='Pessoal, tenho uma entrevista técnica na próxima semana e estou nervoso. '
                    'Alguém pode dar dicas de como me preparar?',
            categoria='Entrevistas',
            urgencia='Alta',
            tags=['entrevista', 'preparacao', 'dicas']
        )
        print(f"✅ Tópico de dúvida criado: {topico_duvida.titulo}")
        print(f"   Conteúdo: {topico_duvida.conteudo[:100]}...")
    except Exception as e:
        print(f"❌ Erro ao criar tópico de dúvida: {e}")
    
    # 3. CRIAR TÓPICO DE EXPERIÊNCIA
    print("\n3. 📖 Criando Tópico de Experiência...")
    try:
        topico_experiencia = TopicoFactory.create_topico(
            tipo_topico='experiencia',
            user=user,
            titulo='Minha experiência na startup XYZ',
            conteudo='Quero compartilhar minha experiência como estagiário na startup XYZ. '
                    'Foi uma experiência incrível onde aprendi muito sobre desenvolvimento ágil.',
            empresa='Startup XYZ',
            periodo='6 meses (Jan-Jun 2024)',
            area='Desenvolvimento de Software',
            nota_experiencia=5
        )
        print(f"✅ Tópico de experiência criado: {topico_experiencia.titulo}")
        print(f"   Conteúdo: {topico_experiencia.conteudo[:100]}...")
    except Exception as e:
        print(f"❌ Erro ao criar tópico de experiência: {e}")
    
    # 4. CRIAR TÓPICO DE DICA
    print("\n4. 💡 Criando Tópico de Dica...")
    try:
        topico_dica = TopicoFactory.create_topico(
            tipo_topico='dica',
            user=user,
            titulo='Como organizar seu tempo durante o estágio',
            conteudo='Baseado na minha experiência, vou compartilhar algumas dicas de como '
                    'organizar o tempo e ser mais produtivo durante o estágio.',
            categoria_dica='Produtividade',
            nivel='Iniciante',
            aplicabilidade='Todos os estágios'
        )
        print(f"✅ Tópico de dica criado: {topico_dica.titulo}")
        print(f"   Conteúdo: {topico_dica.conteudo[:100]}...")
    except Exception as e:
        print(f"❌ Erro ao criar tópico de dica: {e}")
    
    # 5. CRIAR TÓPICO DE DISCUSSÃO
    print("\n5. 🗣️ Criando Tópico de Discussão...")
    try:
        topico_discussao = TopicoFactory.create_topico(
            tipo_topico='discussao',
            user=user,
            titulo='Home office para estagiários: prós e contras',
            conteudo='Com o aumento do trabalho remoto, gostaria de discutir os prós e contras '
                    'do home office especificamente para estagiários. O que vocês acham?',
            tema='Trabalho Remoto',
            tipo_discussao='Debate'
        )
        print(f"✅ Tópico de discussão criado: {topico_discussao.titulo}")
        print(f"   Conteúdo: {topico_discussao.conteudo[:100]}...")
    except Exception as e:
        print(f"❌ Erro ao criar tópico de discussão: {e}")
    
    # 6. DEMONSTRAR TRATAMENTO DE ERRO
    print("\n6. ⚠️ Testando Tratamento de Erros...")
    try:
        TopicoFactory.create_topico(
            tipo_topico='tipo_inexistente',
            user=user,
            titulo='Teste',
            conteudo='Teste de erro'
        )
    except ValueError as e:
        print(f"✅ Erro capturado corretamente: {e}")
    
    # Testar validação de conteúdo
    try:
        TopicoFactory.create_topico(
            tipo_topico='duvida',
            user=user,
            titulo='x',  # Título muito curto
            conteudo='abc'  # Conteúdo muito curto
        )
    except ValueError as e:
        print(f"✅ Validação funcionando: {e}")


def listar_topicos_por_tipo():
    """
    Lista os tópicos agrupados por tipo
    """
    from Forum.models import Forum
    
    print("\n=== Listando Tópicos por Tipo ===")
    
    topicos = Forum.objects.all().order_by('-data_criacao')
    
    tipos = {
        'vaga': [],
        'duvida': [],
        'experiencia': [],
        'dica': [],
        'discussao': [],
        'outros': []
    }
    
    for topico in topicos:
        titulo = topico.titulo.lower()
        if '[vaga' in titulo:
            tipos['vaga'].append(topico)
        elif '[dúvida' in titulo or '[duvida' in titulo:
            tipos['duvida'].append(topico)
        elif '[experiência' in titulo or '[experiencia' in titulo:
            tipos['experiencia'].append(topico)
        elif '[dica' in titulo:
            tipos['dica'].append(topico)
        elif '[discussão' in titulo or '[discussao' in titulo:
            tipos['discussao'].append(topico)
        else:
            tipos['outros'].append(topico)
    
    for tipo, lista_topicos in tipos.items():
        if lista_topicos:
            print(f"\n📊 {tipo.upper()}: {len(lista_topicos)} tópicos")
            for topico in lista_topicos[:3]:  # Mostrar apenas os 3 primeiros
                print(f"  - {topico.titulo}")
                print(f"    👁️ {topico.visualizacoes} visualizações | "
                      f"💬 {topico.total_comentarios} comentários")


def demonstrar_tipos_disponiveis():
    """
    Demonstra os tipos de tópicos disponíveis
    """
    print("\n=== Tipos de Tópicos Disponíveis ===")
    
    tipos = TopicoFactory.get_tipos_disponiveis()
    
    for tipo, info in tipos.items():
        print(f"\n🏷️ **{tipo.upper()}**: {info['nome']}")
        print(f"   📝 {info['descricao']}")
        print(f"   🔧 Campos extras: {', '.join(info['campos_extras'])}")
        print(f"   💡 Exemplo: \"{info['exemplo']}\"")


if __name__ == "__main__":
    demonstrar_tipos_disponiveis()
    print("\n" + "="*60)
    exemplo_uso_topico_factory()
    print("\n" + "="*60)
    listar_topicos_por_tipo()

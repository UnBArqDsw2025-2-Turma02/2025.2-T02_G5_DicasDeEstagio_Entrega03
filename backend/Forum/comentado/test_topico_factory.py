from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from instituicao.models import Instituicao
from Forum.factories.topico_factory import TopicoFactory
from Forum.models import Forum


class Command(BaseCommand):
    help = 'Testa o Factory Method para criação de tópicos do fórum'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--criar-exemplos',
            action='store_true',
            help='Criar tópicos de exemplo para todos os tipos',
        )
        parser.add_argument(
            '--tipo',
            type=str,
            help='Criar apenas um tipo específico de tópico',
            choices=['vaga', 'duvida', 'experiencia', 'dica', 'discussao']
        )
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpar todos os tópicos criados pelo factory antes de criar novos',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== Testando Factory Method para Tópicos ==="))
        
        # Verificar se existem usuários
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("❌ Nenhum usuário encontrado. Crie um usuário primeiro."))
            return
        
        self.stdout.write(f"👤 Usando usuário: {user.email}")
        
        # Limpar tópicos se solicitado
        if options['limpar']:
            self.limpar_topicos_factory()
        
        # Mostrar tipos disponíveis
        self.mostrar_tipos_disponiveis()
        
        # Criar exemplos
        if options['criar_exemplos']:
            self.criar_todos_exemplos(user)
        elif options['tipo']:
            self.criar_exemplo_especifico(user, options['tipo'])
        else:
            self.stdout.write(self.style.WARNING("💡 Use --criar-exemplos ou --tipo=<tipo> para criar tópicos"))
        
        # Mostrar estatísticas finais
        self.mostrar_estatisticas()
    
    def mostrar_tipos_disponiveis(self):
        """Mostra os tipos de tópicos disponíveis"""
        self.stdout.write("\n📋 Tipos de Tópicos Disponíveis:")
        tipos = TopicoFactory.get_tipos_disponiveis()
        
        for tipo, info in tipos.items():
            self.stdout.write(f"  🏷️ {tipo.upper()}: {info['nome']}")
            self.stdout.write(f"     📝 {info['descricao']}")
            self.stdout.write(f"     🔧 Campos: {', '.join(info['campos_extras'])}")
            self.stdout.write("")
    
    def limpar_topicos_factory(self):
        """Remove tópicos criados pelo factory"""
        prefixos = ['[VAGA', '[DÚVIDA', '[EXPERIÊNCIA', '[DICA', '[DISCUSSÃO']
        
        for prefixo in prefixos:
            count = Forum.objects.filter(titulo__startswith=prefixo).count()
            if count > 0:
                Forum.objects.filter(titulo__startswith=prefixo).delete()
                self.stdout.write(f"🗑️ Removidos {count} tópicos do tipo {prefixo}")
    
    def criar_todos_exemplos(self, user):
        """Cria exemplos de todos os tipos de tópicos"""
        self.stdout.write("\n🚀 Criando exemplos de todos os tipos...")
        
        exemplos = [
            ('vaga', self.criar_exemplo_vaga),
            ('duvida', self.criar_exemplo_duvida),
            ('experiencia', self.criar_exemplo_experiencia),
            ('dica', self.criar_exemplo_dica),
            ('discussao', self.criar_exemplo_discussao)
        ]
        
        for tipo, metodo in exemplos:
            try:
                topico = metodo(user)
                self.stdout.write(f"✅ {tipo.upper()}: {topico.titulo}")
            except Exception as e:
                self.stdout.write(f"❌ Erro ao criar {tipo}: {e}")
    
    def criar_exemplo_especifico(self, user, tipo):
        """Cria um exemplo de tipo específico"""
        self.stdout.write(f"\n🎯 Criando exemplo do tipo: {tipo.upper()}")
        
        metodos = {
            'vaga': self.criar_exemplo_vaga,
            'duvida': self.criar_exemplo_duvida,
            'experiencia': self.criar_exemplo_experiencia,
            'dica': self.criar_exemplo_dica,
            'discussao': self.criar_exemplo_discussao
        }
        
        try:
            topico = metodos[tipo](user)
            self.stdout.write(f"✅ Criado: {topico.titulo}")
        except Exception as e:
            self.stdout.write(f"❌ Erro: {e}")
    
    def criar_exemplo_vaga(self, user):
        """Cria exemplo de tópico de vaga"""
        return TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=user,
            titulo='Desenvolvedor Python Júnior',
            conteudo='Estamos buscando um desenvolvedor Python júnior para integrar nossa equipe de tecnologia. '
                    'A pessoa será responsável por desenvolver APIs REST usando Django e trabalhar com bancos de dados PostgreSQL.',
            salario='R$ 2.500,00 - R$ 3.500,00',
            requisitos='Python, Django, Git, PostgreSQL, conhecimento em testes unitários',
            empresa='TechStart Solutions',
            tipo_vaga='Estágio'
        )
    
    def criar_exemplo_duvida(self, user):
        """Cria exemplo de tópico de dúvida"""
        return TopicoFactory.create_topico(
            tipo_topico='duvida',
            user=user,
            titulo='Como me preparar para entrevista técnica em Python?',
            conteudo='Pessoal, tenho uma entrevista técnica para uma vaga de desenvolvedor Python na próxima semana. '
                    'É minha primeira entrevista técnica e estou bem nervoso. Alguém pode me dar dicas do que estudar?',
            categoria='Entrevistas',
            urgencia='Alta',
            tags=['python', 'entrevista', 'preparacao', 'dicas']
        )
    
    def criar_exemplo_experiencia(self, user):
        """Cria exemplo de tópico de experiência"""
        return TopicoFactory.create_topico(
            tipo_topico='experiencia',
            user=user,
            titulo='Minha experiência como estagiário na Startup XYZ',
            conteudo='Quero compartilhar minha experiência de 6 meses como estagiário de desenvolvimento na Startup XYZ. '
                    'Foi uma experiência incrível onde aprendi muito sobre metodologias ágeis, trabalho em equipe e tecnologias modernas.',
            empresa='Startup XYZ',
            periodo='Janeiro 2024 - Junho 2024 (6 meses)',
            area='Desenvolvimento de Software',
            nota_experiencia=5
        )
    
    def criar_exemplo_dica(self, user):
        """Cria exemplo de tópico de dica"""
        return TopicoFactory.create_topico(
            tipo_topico='dica',
            user=user,
            titulo='Como organizar seu tempo durante o estágio',
            conteudo='Baseado na minha experiência, vou compartilhar 5 dicas essenciais para organizar seu tempo '
                    'e ser mais produtivo durante o estágio: 1) Use um aplicativo de gestão de tarefas...',
            categoria_dica='Produtividade',
            nivel='Iniciante',
            aplicabilidade='Todos os tipos de estágio'
        )
    
    def criar_exemplo_discussao(self, user):
        """Cria exemplo de tópico de discussão"""
        return TopicoFactory.create_topico(
            tipo_topico='discussao',
            user=user,
            titulo='Home office para estagiários: vantagens e desvantagens',
            conteudo='Com o aumento do trabalho remoto pós-pandemia, muitas empresas oferecem estágios em home office. '
                    'Gostaria de discutir com vocês: quais são as principais vantagens e desvantagens do home office para estagiários?',
            tema='Trabalho Remoto',
            tipo_discussao='Debate Aberto'
        )
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas dos tópicos"""
        self.stdout.write("\n📊 Estatísticas dos Tópicos:")
        
        prefixos = {
            'VAGA': '[VAGA',
            'DÚVIDA': '[DÚVIDA',
            'EXPERIÊNCIA': '[EXPERIÊNCIA',
            'DICA': '[DICA',
            'DISCUSSÃO': '[DISCUSSÃO'
        }
        
        total_geral = 0
        for nome, prefixo in prefixos.items():
            count = Forum.objects.filter(titulo__startswith=prefixo).count()
            total_geral += count
            self.stdout.write(f"  {nome}: {count} tópicos")
        
        outros = Forum.objects.exclude(
            titulo__regex=r'^\[(VAGA|DÚVIDA|EXPERIÊNCIA|DICA|DISCUSSÃO)'
        ).count()
        
        total_geral += outros
        
        self.stdout.write(f"  OUTROS: {outros} tópicos")
        self.stdout.write(f"  TOTAL: {total_geral} tópicos")
        
        if total_geral > 0:
            self.stdout.write(f"\n🎉 Factory Method funcionando perfeitamente!")
        else:
            self.stdout.write(f"\n⚠️ Nenhum tópico encontrado. Use --criar-exemplos")

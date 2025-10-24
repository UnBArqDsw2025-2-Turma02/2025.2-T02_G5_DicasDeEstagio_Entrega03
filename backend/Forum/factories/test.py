from django.test import TestCase
from django.utils import timezone
from users.models import User
from instituicao.models import Instituicao
from Forum.models import Forum
from Forum.factories.topico_factory import (
    TopicoFactory, 
    TopicoVagaCreator, 
    TopicoDuvidaCreator,
    TopicoExperienciaCreator,
    TopicoDicaCreator,
    TopicoDiscussaoCreator
)


class TopicoFactoryTestCase(TestCase):
    """
    Testes para o padrão Factory Method aplicado aos tópicos do fórum
    """
    
    def setUp(self):
        """Configuração inicial dos testes"""
        # Criar usuário de teste
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Usuário Teste',
            password='testpass123',
            role='estudante'
        )
        
        # Criar instituição de teste
        self.instituicao = Instituicao.objects.create(
            nome='Empresa Teste',
            cnpj='12345678901234',
            AreaAtuacao='Tecnologia'
        )
    
    def test_criar_topico_vaga(self):
        """Testa a criação de tópico de vaga"""
        topico = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=self.user,
            titulo='Desenvolvedor Python',
            conteudo='Vaga para desenvolvedor Python júnior',
            salario='R$ 2.500,00',
            requisitos='Python, Django',
            empresa='Tech Corp',
            tipo_vaga='Estágio'
        )
        
        self.assertIsInstance(topico, Forum)
        self.assertEqual(topico.user, self.user)
        self.assertIn('[VAGA - ESTÁGIO]', topico.titulo)
        self.assertIn('**Empresa:** Tech Corp', topico.conteudo)
        self.assertIn('**Salário:** R$ 2.500,00', topico.conteudo)
        self.assertIn('**Requisitos:** Python, Django', topico.conteudo)
        self.assertTrue(topico.is_active)
    
    def test_criar_topico_duvida(self):
        """Testa a criação de tópico de dúvida"""
        topico = TopicoFactory.create_topico(
            tipo_topico='duvida',
            user=self.user,
            titulo='Como fazer entrevista?',
            conteudo='Preciso de dicas para entrevista técnica',
            categoria='Entrevistas',
            urgencia='Alta',
            tags=['entrevista', 'dicas']
        )
        
        self.assertIsInstance(topico, Forum)
        self.assertIn('[DÚVIDA - ENTREVISTAS]', topico.titulo)
        self.assertIn('**Categoria:** Entrevistas', topico.conteudo)
        self.assertIn('**Urgência:** Alta', topico.conteudo)
        self.assertIn('**Tags:** entrevista, dicas', topico.conteudo)
        self.assertIn('**URGENTE:**', topico.conteudo)
    
    def test_criar_topico_experiencia(self):
        """Testa a criação de tópico de experiência"""
        topico = TopicoFactory.create_topico(
            tipo_topico='experiencia',
            user=self.user,
            titulo='Minha experiência na empresa X',
            conteudo='Quero compartilhar minha experiência de estágio',
            empresa='Empresa X',
            periodo='6 meses',
            area='Desenvolvimento',
            nota_experiencia=4
        )
        
        self.assertIsInstance(topico, Forum)
        self.assertIn('[EXPERIÊNCIA]', topico.titulo)
        self.assertIn('**Empresa:** Empresa X', topico.conteudo)
        self.assertIn('**Período:** 6 meses', topico.conteudo)
        self.assertIn('**Área:** Desenvolvimento', topico.conteudo)
        self.assertIn('⭐⭐⭐⭐ (4/5)', topico.conteudo)
    
    def test_criar_topico_dica(self):
        """Testa a criação de tópico de dica"""
        topico = TopicoFactory.create_topico(
            tipo_topico='dica',
            user=self.user,
            titulo='Como se organizar no estágio',
            conteudo='Dicas de organização para estagiários',
            categoria_dica='Produtividade',
            nivel='Iniciante',
            aplicabilidade='Geral'
        )
        
        self.assertIsInstance(topico, Forum)
        self.assertIn('[DICA - PRODUTIVIDADE]', topico.titulo)
        self.assertIn('**Categoria:** Produtividade', topico.conteudo)
        self.assertIn('**Nível:** Iniciante', topico.conteudo)
        self.assertIn('**Perfeito para quem está começando!**', topico.conteudo)
    
    def test_criar_topico_discussao(self):
        """Testa a criação de tópico de discussão"""
        topico = TopicoFactory.create_topico(
            tipo_topico='discussao',
            user=self.user,
            titulo='Home office para estagiários',
            conteudo='Vamos discutir sobre trabalho remoto',
            tema='Trabalho Remoto',
            tipo_discussao='Debate'
        )
        
        self.assertIsInstance(topico, Forum)
        self.assertIn('[DISCUSSÃO - TRABALHO REMOTO]', topico.titulo)
        self.assertIn('**Tema:** Trabalho Remoto', topico.conteudo)
        self.assertIn('**Tipo:** Debate', topico.conteudo)
    
    def test_tipo_topico_inexistente(self):
        """Testa o tratamento de erro para tipo de tópico inexistente"""
        with self.assertRaises(ValueError) as context:
            TopicoFactory.create_topico(
                tipo_topico='tipo_inexistente',
                user=self.user,
                titulo='Teste',
                conteudo='Conteúdo de teste'
            )
        
        self.assertIn("não suportado", str(context.exception))
    
    def test_validacao_titulo_curto(self):
        """Testa a validação de título muito curto"""
        with self.assertRaises(ValueError) as context:
            TopicoFactory.create_topico(
                tipo_topico='duvida',
                user=self.user,
                titulo='x',  # Título muito curto
                conteudo='Conteúdo válido para teste'
            )
        
        self.assertIn("pelo menos 5 caracteres", str(context.exception))
    
    def test_validacao_conteudo_curto(self):
        """Testa a validação de conteúdo muito curto"""
        with self.assertRaises(ValueError) as context:
            TopicoFactory.create_topico(
                tipo_topico='duvida',
                user=self.user,
                titulo='Título válido para teste',
                conteudo='abc'  # Conteúdo muito curto
            )
        
        self.assertIn("pelo menos 10 caracteres", str(context.exception))
    
    def test_get_creator_direto(self):
        """Testa o uso de creators específicos diretamente"""
        creator = TopicoFactory.get_creator('vaga')
        self.assertIsInstance(creator, TopicoVagaCreator)
        
        creator = TopicoFactory.get_creator('duvida')
        self.assertIsInstance(creator, TopicoDuvidaCreator)
        
        creator = TopicoFactory.get_creator('experiencia')
        self.assertIsInstance(creator, TopicoExperienciaCreator)

    def test_formatacao_titulo_com_prefixo(self):
        """Testa se o prefixo é adicionado corretamente ao título"""
        topico = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=self.user,
            titulo='Desenvolvedor',
            conteudo='Descrição da vaga de desenvolvedor',
            tipo_vaga='CLT'
        )
        
        self.assertEqual(topico.titulo, '[VAGA - CLT] Desenvolvedor')
    
    def test_titulo_ja_com_prefixo(self):
        """Testa que não duplica prefixo se título já tem um"""
        topico = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=self.user,
            titulo='[VAGA - ESTÁGIO] Desenvolvedor',
            conteudo='Descrição da vaga de desenvolvedor',
            tipo_vaga='Estágio'
        )
        
        # Não deve duplicar o prefixo
        self.assertEqual(topico.titulo, '[VAGA - ESTÁGIO] Desenvolvedor')
    
    def test_get_tipos_disponiveis(self):
        """Testa se retorna todos os tipos disponíveis"""
        tipos = TopicoFactory.get_tipos_disponiveis()
        
        self.assertIn('vaga', tipos)
        self.assertIn('duvida', tipos)
        self.assertIn('experiencia', tipos)
        self.assertIn('dica', tipos)
        self.assertIn('discussao', tipos)
        
        # Verificar estrutura dos dados
        for tipo, info in tipos.items():
            self.assertIn('nome', info)
            self.assertIn('descricao', info)
            self.assertIn('campos_extras', info)
            self.assertIn('exemplo', info)
    
    def test_contagem_topicos_por_tipo(self):
        """Testa se diferentes tipos de tópicos são criados corretamente"""
        # Criar um tópico de cada tipo
        TopicoFactory.create_topico('vaga', self.user, 'Vaga teste', 'Conteúdo vaga')
        TopicoFactory.create_topico('duvida', self.user, 'Dúvida teste', 'Conteúdo dúvida')
        TopicoFactory.create_topico('experiencia', self.user, 'Experiência teste', 'Conteúdo experiência')
        TopicoFactory.create_topico('dica', self.user, 'Dica teste', 'Conteúdo dica')
        TopicoFactory.create_topico('discussao', self.user, 'Discussão teste', 'Conteúdo discussão')
        
        # Verificar se foram criados 5 tópicos
        total_topicos = Forum.objects.count()
        self.assertEqual(total_topicos, 5)
        
        # Verificar se cada tipo tem sua marcação específica
        topicos = Forum.objects.all()
        titulos = [t.titulo for t in topicos]
        
        self.assertTrue(any('[VAGA' in t for t in titulos))
        self.assertTrue(any('[DÚVIDA' in t for t in titulos))
        self.assertTrue(any('[EXPERIÊNCIA' in t for t in titulos))
        self.assertTrue(any('[DICA' in t for t in titulos))
        self.assertTrue(any('[DISCUSSÃO' in t for t in titulos))
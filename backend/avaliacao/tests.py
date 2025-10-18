from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from instituicao.models import Instituicao
from .models import Avaliacao
from .factories.avaliacao_factory import AvaliacaoFactory, AvaliacaoEstagioCreator, AvaliacaoEmpresaCreator


class AvaliacaoFactoryTestCase(TestCase):
    """
    Testes para o padrão Factory Method aplicado às avaliações
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
    
    def test_criar_avaliacao_estagio(self):
        """Testa a criação de avaliação de estágio"""
        data_inicio = timezone.now() - timedelta(days=90)
        data_fim = timezone.now() - timedelta(days=10)
        
        avaliacao = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='estagio',
            user=self.user,
            nota=4,
            comentario='Excelente experiência de estágio',
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        self.assertIsInstance(avaliacao, Avaliacao)
        self.assertEqual(avaliacao.nota, 4)
        self.assertEqual(avaliacao.user, self.user)
        self.assertIn('[ESTÁGIO]', avaliacao.comentario)
        self.assertEqual(avaliacao.datainicio, data_inicio)
        self.assertEqual(avaliacao.datafim, data_fim)
    
    def test_criar_avaliacao_empresa(self):
        """Testa a criação de avaliação de empresa"""
        avaliacao = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='empresa',
            user=self.user,
            nota=5,
            comentario='Ótima empresa para trabalhar',
            instituicao=self.instituicao
        )
        
        self.assertIsInstance(avaliacao, Avaliacao)
        self.assertEqual(avaliacao.nota, 5)
        self.assertEqual(avaliacao.user, self.user)
        self.assertIn('[EMPRESA]', avaliacao.comentario)
        self.assertIn(self.instituicao.nome, avaliacao.comentario)
    
    def test_criar_avaliacao_processo_seletivo(self):
        """Testa a criação de avaliação de processo seletivo"""
        avaliacao = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='processo_seletivo',
            user=self.user,
            nota=3,
            comentario='Processo bem estruturado',
            tipo_processo='Dinâmica de Grupo'
        )
        
        self.assertIsInstance(avaliacao, Avaliacao)
        self.assertEqual(avaliacao.nota, 3)
        self.assertEqual(avaliacao.user, self.user)
        self.assertIn('[PROCESSO SELETIVO - DINÂMICA DE GRUPO]', avaliacao.comentario)
    
    def test_tipo_avaliacao_inexistente(self):
        """Testa o tratamento de erro para tipo de avaliação inexistente"""
        with self.assertRaises(ValueError) as context:
            AvaliacaoFactory.create_avaliacao(
                tipo_avaliacao='tipo_inexistente',
                user=self.user,
                nota=3,
                comentario='Teste'
            )
        
        self.assertIn("não suportado", str(context.exception))
    
    def test_validacao_nota_invalida(self):
        """Testa a validação de nota inválida"""
        with self.assertRaises(ValueError) as context:
            AvaliacaoFactory.create_avaliacao(
                tipo_avaliacao='estagio',
                user=self.user,
                nota=6,  # Nota inválida
                comentario='Teste'
            )
        
        self.assertIn("entre 1 e 5", str(context.exception))
        
        # Testar nota negativa
        with self.assertRaises(ValueError):
            AvaliacaoFactory.create_avaliacao(
                tipo_avaliacao='estagio',
                user=self.user,
                nota=-1,
                comentario='Teste'
            )
    
    def test_get_creator_direto(self):
        """Testa o uso de creators específicos diretamente"""
        creator = AvaliacaoFactory.get_creator('estagio')
        self.assertIsInstance(creator, AvaliacaoEstagioCreator)
        
        creator = AvaliacaoFactory.get_creator('empresa')
        self.assertIsInstance(creator, AvaliacaoEmpresaCreator)
    
    def test_avaliacao_estagio_com_datas_padrao(self):
        """Testa criação de avaliação de estágio com datas padrão"""
        avaliacao = AvaliacaoFactory.create_avaliacao(
            tipo_avaliacao='estagio',
            user=self.user,
            nota=4,
            comentario='Teste com datas padrão'
            # Não passar data_inicio nem data_fim
        )
        
        # Verificar se as datas foram definidas automaticamente
        self.assertIsNotNone(avaliacao.datainicio)
        self.assertIsNotNone(avaliacao.datafim)
        self.assertLess(avaliacao.datainicio, avaliacao.datafim)
    
    def test_contagem_avaliacoes_por_tipo(self):
        """Testa se diferentes tipos de avaliação são criados corretamente"""
        # Criar uma avaliação de cada tipo
        AvaliacaoFactory.create_avaliacao('estagio', self.user, 4, 'Estágio teste')
        AvaliacaoFactory.create_avaliacao('empresa', self.user, 5, 'Empresa teste')
        AvaliacaoFactory.create_avaliacao('processo_seletivo', self.user, 3, 'Processo teste')
        
        # Verificar se foram criadas 3 avaliações
        total_avaliacoes = Avaliacao.objects.count()
        self.assertEqual(total_avaliacoes, 3)
        
        # Verificar se cada tipo tem sua marcação específica
        avaliacoes = Avaliacao.objects.all()
        comentarios = [av.comentario for av in avaliacoes]
        
        self.assertTrue(any('[ESTÁGIO]' in c for c in comentarios))
        self.assertTrue(any('[EMPRESA]' in c for c in comentarios))
        self.assertTrue(any('[PROCESSO SELETIVO' in c for c in comentarios))

from django.test import TestCase
from users.models import User
from Forum.models import Forum
from Forum.iterators.forum_iterators import (
    ForumCollection,
    TopicoPorTipoIterator
)
from Forum.factories.topico_factory import TopicoFactory


class TopicoPorTipoIteratorTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            role='estudante'
        )
        
        self.topico_vaga = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=self.user,
            titulo='Vaga Desenvolvedor',
            conteudo='Vaga para desenvolvedor Python',
            empresa='Tech Corp'
        )
        
        self.topico_duvida = TopicoFactory.create_topico(
            tipo_topico='duvida',
            user=self.user,
            titulo='Dúvida sobre entrevistas',
            conteudo='Como me preparar para entrevista técnica?',
            categoria='Carreira'
        )
    
    def test_iterator_filtra_por_tipo_vaga(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset, 'vaga')
        
        self.assertEqual(iterator.get_total(), 1)
        self.assertTrue(iterator.has_next())
        
        topico = iterator.next()
        self.assertIn('[VAGA', topico.titulo)
        self.assertEqual(topico.id, self.topico_vaga.id)
        
        self.assertFalse(iterator.has_next())
    
    def test_iterator_filtra_por_tipo_duvida(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset, 'duvida')
        
        self.assertEqual(iterator.get_total(), 1)
        topico = iterator.next()
        self.assertIn('[DÚVIDA', topico.titulo)
    
    def test_iterator_reset_functionality(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset, 'vaga')
        
        primeiro_topico = iterator.next()
        self.assertFalse(iterator.has_next())
        
        iterator.reset()
        self.assertTrue(iterator.has_next())
        segundo_topico = iterator.next()
        
        self.assertEqual(primeiro_topico.id, segundo_topico.id)
    
    def test_iterator_sem_filtro_tipo(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset)
        
        self.assertEqual(iterator.get_total(), 2)
    
    def test_iterator_current_method(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset, 'vaga')
        
        self.assertIsNone(iterator.current())
        
        topico = iterator.next()
        current_topico = iterator.current()
        
        self.assertEqual(topico.id, current_topico.id)
    
    def test_iterator_stop_iteration(self):
        queryset = Forum.objects.all()
        iterator = TopicoPorTipoIterator(queryset, 'vaga')
        
        iterator.next()
        
        with self.assertRaises(StopIteration):
            iterator.next()


class ForumCollectionTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            role='estudante'
        )
        
        self.topico_vaga = TopicoFactory.create_topico(
            tipo_topico='vaga',
            user=self.user,
            titulo='Vaga de teste',
            conteudo='Conteúdo da vaga'
        )
    
    def test_collection_create_iterator_por_tipo(self):
        collection = ForumCollection()
        iterator = collection.create_iterator_por_tipo('vaga')
        
        self.assertIsInstance(iterator, TopicoPorTipoIterator)
        self.assertEqual(iterator.get_total(), 1)
    
    def test_collection_get_total_count(self):
        collection = ForumCollection()
        self.assertEqual(collection.get_total_count(), 1)


class IteratorIntegrationTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            role='estudante'
        )
    
    def test_factory_method_iterator_integration(self):
        tipos_topicos = ['vaga', 'duvida', 'dica']
        
        for tipo in tipos_topicos:
            TopicoFactory.create_topico(
                tipo_topico=tipo,
                user=self.user,
                titulo=f'Teste {tipo}',
                conteudo=f'Conteúdo de teste para {tipo}'
            )
        
        collection = ForumCollection()
        
        for tipo in tipos_topicos:
            iterator = collection.create_iterator_por_tipo(tipo)
            self.assertEqual(iterator.get_total(), 1, f"Deveria ter 1 tópico do tipo {tipo}")
            
            if iterator.has_next():
                topico = iterator.next()
                self.assertIn(tipo.upper(), topico.titulo.upper())
    
    def test_workflow_completo_minimo(self):
        for i in range(3):
            TopicoFactory.create_topico(
                tipo_topico='vaga',
                user=self.user,
                titulo=f'Vaga {i+1}',
                conteudo=f'Descrição da vaga {i+1}',
                empresa=f'Empresa {i+1}'
            )
        
        collection = ForumCollection()
        iterator = collection.create_iterator_por_tipo('vaga')
        
        vagas_encontradas = []
        while iterator.has_next():
            vaga = iterator.next()
            vagas_encontradas.append(vaga)
        
        self.assertEqual(len(vagas_encontradas), 3)
        
        for vaga in vagas_encontradas:
            self.assertIn('[VAGA', vaga.titulo)

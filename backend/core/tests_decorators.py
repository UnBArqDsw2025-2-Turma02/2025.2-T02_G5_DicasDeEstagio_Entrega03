import json
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response

from core.decorators import log_request, LoggingDecorator

User = get_user_model()


def get_json_data(response):
    return json.loads(response.content.decode('utf-8'))


class LoggingDecoratorTestCase(TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.factory = RequestFactory()
        
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            role='empresa',
            password='test123'
        )
    
    def test_logging_decorator_executes_view(self):
        """Testa se o LoggingDecorator executa a view corretamente"""
        
        @log_request
        def test_view(request):
            return JsonResponse({'message': 'success', 'status': 'ok'})
        
        request = self.factory.get('/test/')
        request.user = self.user
        
        response = test_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(data['status'], 'ok')
    
    def test_logging_decorator_with_authenticated_user(self):
        
        @log_request
        def test_view(request):
            return JsonResponse({'user': request.user.email})
        
        request = self.factory.get('/api/forum/')
        request.user = self.user
        
        response = test_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user'], 'test@example.com')
    
    def test_logging_decorator_with_anonymous_user(self):
        from django.contrib.auth.models import AnonymousUser
        
        @log_request
        def test_view(request):
            return JsonResponse({'message': 'public'})
        
        request = self.factory.get('/api/forum/')
        request.user = AnonymousUser()
        
        response = test_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'public')
    
    def test_logging_decorator_with_post_request(self):
        
        @log_request
        def test_view(request):
            return JsonResponse({'method': request.method})
        
        request = self.factory.post('/api/forum/')
        request.user = self.user
        
        response = test_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['method'], 'POST')
    
    def test_logging_decorator_with_exception(self):
        
        @log_request
        def test_view(request):
            raise ValueError("Test error message")
        
        request = self.factory.get('/test/')
        request.user = self.user
        
        with self.assertRaises(ValueError) as context:
            test_view(request)
        
        self.assertEqual(str(context.exception), "Test error message")
    
    def test_logging_decorator_preserves_response_data(self):
        
        @log_request
        def test_view(request):
            return JsonResponse({
                'id': 1,
                'titulo': 'Test Topic',
                'conteudo': 'Test content',
                'user': request.user.email
            })
        
        request = self.factory.get('/api/forum/1/')
        request.user = self.user
        
        response = test_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['titulo'], 'Test Topic')
        self.assertEqual(data['conteudo'], 'Test content')
        self.assertEqual(data['user'], 'test@example.com')
    
    def test_logging_decorator_different_http_methods(self):
        
        @log_request
        def test_view(request):
            return JsonResponse({'method': request.method})
        
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        for method in methods:
            factory_method = getattr(self.factory, method.lower())
            request = factory_method('/api/test/')
            request.user = self.user
            
            response = test_view(request)
            data = get_json_data(response)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['method'], method)
    
    def test_logging_decorator_class_usage(self):
        
        def original_view(request):
            return JsonResponse({'decorated': True})
        
        decorated_view = LoggingDecorator(original_view)
        
        request = self.factory.get('/test/')
        request.user = self.user
        
        response = decorated_view(request)
        data = get_json_data(response)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['decorated'], True)

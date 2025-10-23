import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class ViewDecorator:
    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)
    
    def __call__(self, *args, **kwargs):
        return self.view_func(*args, **kwargs)


class LoggingDecorator(ViewDecorator):
    """
    Decorator para logging de requisições em views do Django/DRF.
    Funciona tanto com function-based views quanto com ViewSet actions.
    """

    def __call__(self, *args, **kwargs):
        # Identificar o request nos argumentos
        request = None
        is_viewset_method = False
        
        # Para métodos de ViewSet: args = (self, request, ...)
        # Para function views: args = (request, ...)
        if len(args) >= 2:
            # Verificar se o segundo argumento é request (caso ViewSet)
            if hasattr(args[1], 'user') and hasattr(args[1], 'method'):
                request = args[1]
                is_viewset_method = True
        
        if request is None and len(args) >= 1:
            # Verificar se o primeiro argumento é request (caso function view)
            if hasattr(args[0], 'user') and hasattr(args[0], 'method'):
                request = args[0]
                is_viewset_method = False
        
        # Se não encontrou request, executa sem logging
        if request is None:
            logger.warning("LoggingDecorator: Request object not found in arguments")
            return self.view_func(*args, **kwargs)
        
        # Início do logging
        start_time = time.time()
        
        user_info = request.user.email if request.user.is_authenticated else 'Anonymous'
        logger.info(
            f"[REQUEST] {request.method} {request.path} - User: {user_info}"
        )
        
        try:
            # Executar a view original
            # Se é método de ViewSet, precisamos passar todos os args
            # Se é function view, também passamos todos
            response = self.view_func(*args, **kwargs)
            
            # Log de sucesso
            execution_time = time.time() - start_time
            status_code = getattr(response, 'status_code', 'N/A')
            
            logger.info(
                f"[RESPONSE] {request.method} {request.path} - "
                f"Status: {status_code} - "
                f"Time: {execution_time:.3f}s - "
                f"User: {user_info}"
            )
            
            return response
            
        except Exception as e:
            # Log de erro
            execution_time = time.time() - start_time
            logger.error(
                f"[ERROR] {request.method} {request.path} - "
                f"Error: {str(e)} - "
                f"Time: {execution_time:.3f}s - "
                f"User: {user_info}",
                exc_info=True  # Inclui stack trace completo
            )
            raise


def log_request(view_func):
    """
    Decorator simplificado para logging de requisições.
    
    Uso:
        @log_request
        @action(detail=False, methods=['post'])
        def minha_action(self, request):
            ...
    """
    return LoggingDecorator(view_func)
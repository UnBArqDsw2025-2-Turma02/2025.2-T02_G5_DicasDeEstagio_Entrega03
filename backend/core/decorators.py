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

    def __call__(self, request, *args, **kwargs):
        start_time = time.time()
        
        user_info = request.user.email if request.user.is_authenticated else 'Anonymous'
        logger.info(
            f"[REQUEST] {request.method} {request.path} - User: {user_info}"
        )
        
        try:
            response = self.view_func(request, *args, **kwargs)
            
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
            execution_time = time.time() - start_time
            logger.error(
                f"[ERROR] {request.method} {request.path} - "
                f"Error: {str(e)} - "
                f"Time: {execution_time:.3f}s - "
                f"User: {user_info}"
            )
            raise  



def log_request(view_func):
    return LoggingDecorator(view_func)

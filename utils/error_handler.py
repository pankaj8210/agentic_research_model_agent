import time
from functools import wraps
from typing import Callable, Any, Dict
from utils.logger import log

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Callable:
    """
    Decorator that retries a function upon failure with exponential backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between attempts in seconds
        backoff: Multiplier for delay between attempts
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        log(f"Operation failed after {attempts} attempts: {str(e)}", "error")
                        raise
                    
                    log(f"Attempt {attempts} failed. Retrying in {current_delay:.1f}s... ({str(e)})", "warning")
                    time.sleep(current_delay)
                    current_delay *= backoff
                    
        return wrapper
    return decorator

class ErrorHandler:
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Standard error handling that returns a structured response
        
        Args:
            error: Exception that was raised
            context: Additional context about where error occurred
            
        Returns:
            Dictionary with error information
        """
        error_type = type(error).__name__
        log(f"Error in {context}: {error_type} - {str(error)}", "error")
        
        return {
            'status': 'error',
            'error_type': error_type,
            'message': str(error),
            'context': context,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
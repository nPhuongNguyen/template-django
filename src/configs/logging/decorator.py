import json
from functools import wraps
from django.http import HttpRequest
from rest_framework.response import Response  
from src.utils.logger import log_error, log_info


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        request = next((arg for arg in args if isinstance(arg, HttpRequest)), None)

        if request:
            log_info(
                func_name=function_name,
                msg=f"View {function_name} được gọi - URL: {request.get_full_path()}"
            )
        else:
            log_info(func_name=function_name, msg=f"Function {function_name} được gọi")

        try:
            return func(*args, **kwargs)

        except json.JSONDecodeError as e:
            log_error(func_name=function_name, error=f"Invalid JSON body - {str(e)}")
            return Response({
                "status": 0,
                "msg": "error",
                "detail": "Invalid JSON body"
            },)

        except ValueError as e:
            log_error(func_name=function_name, error=f"Value error - {str(e)}")
            return Response({
                "status": 0,
                "msg": "error",
                "detail": str(e)
            },)

        except Exception as e:
            log_error(func_name=function_name, error=f"Unexpected error - {str(e)}")
            return Response({
                "status": 0,
                "msg": "error",
                "detail": "An unexpected error occurred"
            },)

    return wrapper

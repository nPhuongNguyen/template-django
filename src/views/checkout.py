from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from src.configs.logging.decorator import handle_exceptions
from src.models.checkout import CheckoutCreate
from src.services.checkout import CheckoutService
from src.utils.auth import TokenAuth
from src.utils.logger import log_info, log_error
from datetime import datetime

class CheckoutView(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = TokenAuth()
        self.checkout_service = CheckoutService()
    
    @action(detail=False, methods=["post"])
    @handle_exceptions
    def checkout_create(self, request: Request):
        function_name = "checkout_create"
        token = self.token.get_token(request)

        checkout_data = CheckoutCreate(**request.data) 

        function_name += f"__{token, checkout_data}__{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        log_info(func_name=function_name, msg=f"Dữ liệu Input: Token: {token}, Data: {checkout_data}", request=request)

        data, errors = self.checkout_service.create_checkout(token, checkout_data, function_name)

        if data:
            log_info(func_name=function_name, msg=f"Data: {data}")
            return Response({"status": 1, "msg": "ok", "detail": data})

        log_error(func_name=function_name, error=f"Errors: {str(errors)}")
        return Response({"status": 0, "msg": "errors", "detail": str(errors)})


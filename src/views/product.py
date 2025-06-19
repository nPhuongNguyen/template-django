from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime

from src.configs.logging.decorator import handle_exceptions
from src.models.product import ProductList, ProductSlug
from src.services.product import ProductService
from src.utils.logger import log_error, log_info


class ProductView(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

        
    @action(detail=False, methods=["post"])
    @handle_exceptions
    def product_list(self, request: Request):
        function_name = "product_list"
        body = request.data
        product_input = ProductList(**body)
        function_name += f"__{product_input.first, product_input.after}__{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        log_info(func_name=function_name, msg=f"Product List Input: first={product_input.first}, after={product_input.after}")
        data, errors = self.product_service.get_all_product_of_channel(first=product_input.first, after=product_input.after, function_name=function_name)
        if errors:
            log_error(func_name=function_name, error=f"Error fetching product list: {str(errors)}", request=request)
            return Response({"status": 0, "msg": "error", "detail": str(errors)}, status=500)

        log_info(func_name=function_name, msg=f"Product List Output: {data}", request=request)
        return Response({"status": 1, "msg": "ok", "detail": data})
    
    @action(detail=False, methods=["post"])
    @handle_exceptions
    def product_slug(self, request: Request):
        function_name = "product_slug"
        body = request.data
        product_input = ProductSlug(**body)

        function_name += f"__{product_input.slug}__{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        log_info(func_name=function_name, msg=f"product_slug Input: {product_input.slug}", request=request)

        data, errors = self.product_service.get_product_by_slug(slug=product_input.slug, function_name=function_name)
        if errors:
            log_info(func_name=function_name, msg=f"product_slug Output Erorrs: {product_input.slug} - {errors}", request=request)
            return Response({
                "status": 0,
                "msg": "error",
                "detail": str(errors)
            },)

        log_info(func_name=function_name, msg=f"product_slug Output: {data}", request=request)
        return Response({"status": 1, "msg": "ok", "detail": data})



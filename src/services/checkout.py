from src.configs.logging.decorator import handle_exceptions
from src.graph_client.checkout import graphql_mutation_checkout_create, variables
from src.graph_client.fetch_graphql_client import fetch_graphql
from src.models.checkout import CheckoutCreate, CheckoutError, CheckoutLine, CheckoutOutputResponse, CheckoutResponse, CheckoutOutput
from src.utils.logger import log_error, log_info

class CheckoutService:
    @handle_exceptions
    def create_checkout(self, token:str, body: CheckoutCreate, function_name: str) ->CheckoutOutput:
        graphql_mutaion = graphql_mutation_checkout_create()
        variables_checkout_create = variables(body)
        log_info(func_name= function_name, msg=f"Dữ liệu Input: Token: {token}, Graphql: {graphql_mutaion}, Variables: {variables_checkout_create}")
        result, errors = fetch_graphql(token = token, graphql_query = graphql_mutaion, variables=variables_checkout_create, function_name=function_name)
        if errors:
            return None, errors
        checkout_response  = CheckoutOutputResponse(**result)
        checkout_response_model = checkout_response.checkoutCreate
        output = outputCheck(checkout_response_model)
        if isinstance(output, list):
            log_error(func_name=function_name, error="Dữ liệu trả về Errors")
            return None, [e.model_dump() for e in output]
        log_info(func_name=function_name, msg="Dữ liệu trả về dạng Checkout hợp lệ")
        return output.model_dump(), None



def outputCheck(body: CheckoutResponse)->CheckoutOutput | list[CheckoutError]:
    checkout = body.checkout
    if checkout is None:
        checkout = body.errors
        return [CheckoutError(field=e.field, code=e.code) for e in body.errors]
    
    lines_output = [
        CheckoutLine(
            quantity=line.quantity,
            variantId=line.variant.id, 
            price=line.totalPrice.gross.amount
        ) for line in checkout.lines
    ]
    return CheckoutOutput(
        id = checkout.id,
        token = checkout.token,
        email = checkout.email,
        lines=lines_output,
        totalPrice = checkout.totalPrice.gross.amount
    )
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError, TransportError
from aiohttp.client_exceptions import ClientConnectorError
import jwt
from hi_ecom_product_api.settings import SALEOR_URL
from src.utils.logger import log_error, log_info


def fetch_graphql(
    token: str,
    graphql_query: str,
    variables: dict,
    function_name: str,
):
    headers = {}
    if token:
        headers["Authorization"] = token

    transport = AIOHTTPTransport(url=SALEOR_URL, headers=headers, timeout=10)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    
    gql_obj = gql(graphql_query)
    try:
        log_info(
            func_name=function_name,
            msg=f"Fetch GraphQL Input: \nToken: {token} \nQuery: {graphql_query}\nVariables: {variables}"
        )
        result = client.execute(gql_obj, variable_values=variables)
        log_info(
            func_name=function_name,
            msg="Fetch GraphQL Success",
            extra={"result_size": len(str(result))}
        )
        return result, None

    except asyncio.TimeoutError:
        error_msg = "GraphQL request timed out"
        log_error(func_name=function_name, error=error_msg)
        return None, error_msg

    except (TransportQueryError, TransportServerError) as e:
        error_msg = f"GraphQL query error: {str(e)}"
        log_error(func_name=function_name, error=error_msg)
        return None, error_msg
        
    except (TransportError, ClientConnectorError, OSError) as e:
        error_msg = f"Network error: {str(e)}"
        log_error(func_name=function_name, error=error_msg)
        return None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        log_error(func_name=function_name, error=error_msg)
        return None, error_msg

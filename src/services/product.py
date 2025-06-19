from src.configs.logging.decorator import handle_exceptions
from src.graph_client.fetch_graphql_client import fetch_graphql
from src.graph_client.product import graphql_query_product_by_slug, graphql_query_product_of_channel, variables_for_product_query
from glom import glom, Coalesce
from src.models.product import Product
from src.utils.logger import log_error, log_info

class ProductService:
    @handle_exceptions
    def get_all_product_of_channel(self, first: int = None, after: str = None, function_name: str = None):
        if function_name is None:
            return None, {"error": "Missing `function_name`"}

        graphql_query = graphql_query_product_of_channel()
        variables = variables_for_product_query(first=first, after=after)

        log_info(func_name=function_name, msg=f"GraphQL Input: first={first}, after={after}, variables={variables}")

        result, errors = fetch_graphql(
            token="",
            graphql_query=graphql_query,
            variables=variables,
            function_name=function_name,
        )

        if errors:
            log_error(func_name=function_name, error=f"GraphQL Error: {errors}")
            return None, errors

        edges = result['products']['edges']
        page_info = result['products']['pageInfo']
        total_count = result['products']['totalCount']

        flatten_products = [flatten_product_node_with_glom(edge['node']) for edge in edges]

        response = {
            "products": [p.model_dump() for p in flatten_products],
            "pageInfo": page_info,
            "totalCount": total_count,
        }

        log_info(func_name=function_name, msg=f"Fetched {len(flatten_products)} products")

        return response, None

    @handle_exceptions
    def get_product_by_slug(self, slug: str, function_name: str):
        graphql_query = graphql_query_product_by_slug()
        variables = variables_for_product_query(slug=slug)

        result, errors = fetch_graphql(
            token="",
            graphql_query=graphql_query,
            variables=variables,
            function_name=function_name,
        )

        if errors:
            log_error(func_name=function_name, error=f"GraphQL Error: {errors}")
            return None, errors

        product_data = result.get('product')
        if product_data is None:
            return None, "Không tìm thấy sản phẩm nào!"

        flattened_product = flatten_product_node_with_glom(product_data)
        return flattened_product.model_dump(), None

def flatten_product_node_with_glom(node: dict) -> Product:
    spec = {
        "id": Coalesce("id", default=None),
        "name": Coalesce("name", default=None),
        "slug": Coalesce("slug", default=None),
        "product_type_name": Coalesce("productType.name", default=None),
        "category_name": Coalesce("category.name", default=None),
        "thumbnail_url": Coalesce("thumbnail.url", default=None),
        "price": Coalesce("pricing.priceRangeUndiscounted.start.gross.amount", default=None),
        "currency": Coalesce("pricing.priceRange.start.gross.currency", default=None),
    }

    flattened = glom(node, spec)
    return Product(
        id=flattened["id"],
        name=flattened["name"],
        slug=flattened["slug"],
        product_type_name=flattened["product_type_name"],
        category_name=flattened["category_name"],
        thumbnail_url=flattened["thumbnail_url"] or "hehehehhe",
        price=flattened["price"],
        currency=flattened["currency"],
    )



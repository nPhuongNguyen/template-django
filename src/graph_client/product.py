def graphql_query_product_of_channel():
    return """
       query($channel: String!, $first: Int, $after: String) {
            products(channel: $channel, first: $first, after: $after) {
                edges {
                    node {
                        id
                        name
                        slug
                        productType {
                            id
                            name
                        }
                        category {
                            id
                            name
                        }
                        thumbnail {
                            url
                        }
                        pricing {
                            priceRangeUndiscounted {
                                start {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                            priceRange {
                                start {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    endCursor
                }
                totalCount
            }
       }
    """

def graphql_query_product_by_slug():
    return """
            query($slug :String!, $channel:String!) {
                product(slug: $slug, channel:$channel) {
                    id
                    name
                    slug
                    productType {
                        id
                        name
                    }
                    category {
                        id
                        name
                    }
                    thumbnail {
                        url
                    }
                    pricing {
                        priceRangeUndiscounted {
                            start {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                        priceRange {
                            start {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                    }  
                }
            }
       """

def variables_for_product_query(first: int = None, after: str = None, slug: str = None, channel: str = None):
    variables = {
        "channel": channel or "hi-fpt",
        "first" : first or 100
    }
    if after:
        variables.update({
            "after": after
        })
    if slug:
        variables.update({
            "slug": slug
        })
    
    return variables




            
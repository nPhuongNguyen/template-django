from src.models.checkout import CheckoutCreate


def graphql_mutation_checkout_create():
    return """
        mutation CheckoutCreate($input: CheckoutCreateInput!) {
            checkoutCreate(input: $input) {
                checkout {
                    id
                    token
                    email
                    lines {
                        id
                        quantity
                        totalPrice {
                            gross {
                                amount
                                currency
                            }
                        }
                        variant {
                            id
                            name
                            product {
                                id
                                name
                                slug
                                thumbnail {
                                    url
                                    alt
                                }
                                category {
                                    name
                                }
                            }
                            pricing {
                                price {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                        }
                    }
                    totalPrice {
                        gross {
                            amount
                            currency
                        }
                    }
                }
                errors {
                    field
                    code
                }
            }
        }
    """

def variables(body: CheckoutCreate):
    return {
        "input": body.model_dump(exclude_none=True)
    }
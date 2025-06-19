from pydantic import BaseModel, ConfigDict, conint
from typing import Optional

class Product(BaseModel):
    id: str
    name: str
    slug: str
    product_type_name: str
    category_name: str
    thumbnail_url: Optional[str]
    price: Optional[float]
    currency: Optional[str]

    model_config = ConfigDict(extra="forbid")


class ProductList(BaseModel):
    first: Optional[conint(ge=1, le=100)] = None
    after: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

class ProductSlug(BaseModel):
    slug : str

    model_config = ConfigDict(extra="forbid")
from typing import List, Optional
from pydantic import BaseModel


class Metadata(BaseModel):
    key: str
    value: str


class Address(BaseModel):
    firstName: str
    lastName: str
    companyName: str
    streetAddress1: str
    streetAddress2: str = None
    city: str
    cityArea: str
    postalCode: str
    country: str
    countryArea: str
    phone: str
    metadata: Optional[List[Metadata]] = []
    skipValidation: Optional[bool] = False


class CheckoutAddressValidationRules(BaseModel):
    checkRequiredFields: bool
    checkFieldsFormat: bool
    enableFieldsNormalization: bool


class CheckoutValidationRules(BaseModel):
    shippingAddress: Optional[CheckoutAddressValidationRules]
    billingAddress: Optional[CheckoutAddressValidationRules]


class CheckoutLine(BaseModel):
    quantity: int
    variantId: str
    price: Optional[float] = None
    forceNewLine: Optional[bool] = False
    metadata: Optional[List[Metadata]] = []


class CheckoutCreate(BaseModel):
    channel: str
    lines: List[CheckoutLine]
    email: Optional[str] = None
    shippingAddress: Optional[Address] = None
    billingAddress: Optional[Address] = None
    languageCode: Optional[str] = None
    validationRules: Optional[CheckoutValidationRules] = None

class Money(BaseModel):
    amount: float
    currency: str


class Price(BaseModel):
    gross: Money


class Category(BaseModel):
    name: str


class Thumbnail(BaseModel):
    url: str
    alt: Optional[str]


class Product(BaseModel):
    id: str
    name: str
    slug: str
    thumbnail: Thumbnail
    category: Category


class VariantPricing(BaseModel):
    price: Price


class Variant(BaseModel):
    id: str
    name: str
    product: Product
    pricing: VariantPricing


class Line(BaseModel):
    id: str
    quantity: int
    totalPrice: Price
    variant: Variant


class CheckoutTotalPrice(BaseModel):
    gross: Money


class Checkout(BaseModel):
    id: str
    token: str
    email: Optional[str]
    lines: List[Line]
    totalPrice: CheckoutTotalPrice


class CheckoutError(BaseModel):
    field: Optional[str]
    code: str


class CheckoutResponse(BaseModel):
    checkout: Optional[Checkout]
    errors: List[CheckoutError]

class CheckoutOutputResponse(BaseModel):
    checkoutCreate: CheckoutResponse

class CheckoutOutput(BaseModel):
    id: str
    token: str
    email: Optional[str]
    lines: List[CheckoutLine]
    totalPrice: float
    
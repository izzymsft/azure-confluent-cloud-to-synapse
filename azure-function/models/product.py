from typing import TypedDict


class Product(TypedDict):
    """
    Represents a Product record in the database
    """
    product_id: int
    product_name: str
    product_price: float
    coupon_code: str
    product_description: str
    active_product: bool

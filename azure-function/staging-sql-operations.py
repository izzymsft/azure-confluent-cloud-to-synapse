from models.product import Product
from shared.product_operations import ProductOperations

operations = ProductOperations()

price: float = 31.44
coupon_code: str = "C'CC"
description = "product's description CC"

products: list[Product] = [
    {"product_id": 6, "product_name": "Rice", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True},
    {"product_id": 7, "product_name": "Beans", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": False},
    {"product_id": 3, "product_name": "Bread", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True},
    {"product_id": 4, "product_name": "Milk", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": False},
    {"product_id": 5, "product_name": "Eggs", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True}
]

result = operations.handle_upsert(products)

# operations.handle_accumulate(products)


from models.product import Product
from shared.product_operations import ProductOperations

operations = ProductOperations()

price: float = 30.44
coupon_code: str = "QBA"
description = "product description 223349"

products: list[Product] = [
    {"product_id": 1, "product_name": "Rice", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True},
    {"product_id": 2, "product_name": "Beans", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": False},
    {"product_id": 3, "product_name": "Bread", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True},
    {"product_id": 4, "product_name": "Milk", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": False},
    {"product_id": 5, "product_name": "Eggs", "product_price": price, "coupon_code": coupon_code, "product_description": description,
     "active_product": True}
]

result = operations.handle_upsert(products)

print(result)

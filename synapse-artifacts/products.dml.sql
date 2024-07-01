

CREATE TABLE product_data
(
    product_id int identity(1, 1) NOT NULL,
    product_name varchar(16),
    product_price float,
    coupon_code varchar(32),
    product_description varchar(max),
    active_product int NOT NULL
);

MERGE INTO [{table_name}] t
USING (VALUES {merge_values}) AS v (product_id, product_name, product_price, coupon_code, product_description, active_product)
ON t.product_id = v.product_id
-- Replace when the key exists
WHEN MATCHED THEN
    UPDATE SET
        t.product_name = v.product_name,
        t.product_price = v.product_price,
        t.coupon_code = v.coupon_code,
        t.product_description = v.product_description,
        t.active_product = v.active_product
-- Insert new keys
WHEN NOT MATCHED BY t THEN
    INSERT (product_id, product_name, product_price, coupon_code, product_description, active_product)
    VALUES (v.product_id, v.product_name, v.product_price, v.coupon_code, v.product_description, v.active_product)

--- Real Records
INSERT INTO contoso_products (product_id, product_name, product_price, coupon_code, product_description, active_product)
VALUES
(16, 'Moi Moi', 30.75, 'APC', 'Moi Moi description', 1);

--- Tombstone Records
INSERT INTO contoso_products (PRODUCT_ID) VALUES (17);
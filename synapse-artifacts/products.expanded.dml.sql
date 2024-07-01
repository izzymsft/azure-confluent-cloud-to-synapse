
INSERT INTO dbo.product_data_expanded
(product_name, product_price, coupon_code, product_description, active_product)
VALUES 
('Pizza', 45.99, 'XYC', 'Amazing Pizza', 1),
('Banana', 45.99, 'XYC', 'Amazing Bananas', 1);


UPDATE dbo.product_data_expanded SET product_price = 2.05 WHERE product_id = 1;

SELECT product_id, date_created, date_modified FROM product_data_expanded
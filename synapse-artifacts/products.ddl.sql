
CREATE TABLE product_data
(
    product_id int identity(1, 1) NOT NULL,
    product_name varchar(16),
    product_price float,
    coupon_code varchar(32),
    product_description varchar(max),
    active_product int NOT NULL
);